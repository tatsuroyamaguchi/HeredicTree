from parameter import ROMAN_TO_INT
from utils import parse_list_string


class PedigreeEngine:
    """Engine for calculating pedigree layout positions."""

    def __init__(self, data, config):
        """Initialize the pedigree engine with data and configuration."""
        self.raw_ind = data.get("individual", [])
        self.raw_rel = data.get("relationships", [])
        self.nodes = {}
        self.generations = {}
        
        # Store configuration
        self.GEN_HEIGHT = config['gen_height']
        self.NODE_WIDTH = config['node_width']
        self.MIN_SIB_SPACING = config['min_sib_spacing']
        self.PARTNER_SPACING = config['partner_spacing']
        self.FAMILY_GAP = config['family_gap']
        
        self._build_graph()
    
    def _is_affected_code(self, nid, code):
        if nid not in self.nodes:
            return False
        vals = parse_list_string(self.nodes[nid]["data"].get("affected", ""))
        return code in vals

    def _is_donor(self, nid):
        """Check if a node is a donor based on 'donor' field or 'affected' field."""
        if nid not in self.nodes:
            return False
        # 変更: まず独立したフィールドを確認し、なければaffectedコードを確認
        is_donor_bool = self.nodes[nid]["data"].get("donor")
        if is_donor_bool is True or str(is_donor_bool).lower() == 'true':
            return True
        return self._is_affected_code(nid, "D")

    def _is_surrogate(self, nid):
        """Check if a node is a surrogate based on 'surrogate' field or 'affected' field."""
        if nid not in self.nodes:
            return False
        
        # 変更: まず独立したフィールドを確認
        is_surrogate_bool = self.nodes[nid]["data"].get("surrogate")
        if is_surrogate_bool is True or str(is_surrogate_bool).lower() == 'true':
            return True
            
        # 互換性のためのフォールバック
        return self._is_affected_code(nid, "S")
    
    def _parse_gen(self, pid):
        prefix = pid.split("-")[0]
        return ROMAN_TO_INT.get(prefix, 1)
    
    def _parse_individual_number(self, pid):
        try:
            return int(pid.split("-")[-1])
        except (ValueError, IndexError):
            return 9999
    
    def _initialize_node(self, person):
        pid = person["id"]
        gen = self._parse_gen(pid)
        
        return {
            "data": person,
            "id": pid,
            "gen": gen,
            "spouse_ids": [],
            "children_ids": [],
            "parent_ids": [],
            "adopted_in": False,
            "adopted_out": False,
            "x": 0.0,
            "y": -(gen * self.GEN_HEIGHT),
            "width_val": self.NODE_WIDTH,
            "sort_idx": self._parse_individual_number(pid)
        }
    
    def _link_partners(self, p1, p2):
        """Link two partners in the graph."""
        if p1 == p2 or p1 not in self.nodes or p2 not in self.nodes:
            return
        
        # Don't link if either is a donor or surrogate (visual separation)
        if self._is_donor(p1) or self._is_donor(p2):
            return
        if self._is_surrogate(p1) or self._is_surrogate(p2):
            return
        
        if p2 not in self.nodes[p1]["spouse_ids"]:
            self.nodes[p1]["spouse_ids"].append(p2)
        if p1 not in self.nodes[p2]["spouse_ids"]:
            self.nodes[p2]["spouse_ids"].append(p1)
    
    def _link_parent_child(self, parent, child):
        """Link parent and child in the graph."""
        if parent not in self.nodes or child not in self.nodes:
            return
        
        # Don't link if parent is a donor (stops them from being pulled together too closely)
        # Note: Surrogates ARE linked to pull child near them, 
        # but _link_partners prevents horizontal adjacency with intended parent.
        if self._is_donor(parent):
            return
        
        if parent not in self.nodes[child]["parent_ids"]:
            self.nodes[child]["parent_ids"].append(parent)
        
        if child not in self.nodes[parent]["children_ids"]:
            self.nodes[parent]["children_ids"].append(child)
    
    def _process_relationship(self, rel):
        p1 = rel.get("p1")
        p2 = rel.get("p2")
        
        if not p1 or p1 not in self.nodes:
            return
        
        if not p2:
            p2 = p1
        if p2 not in self.nodes:
            p2 = p1
        
        self._link_partners(p1, p2)
        
        children = rel.get("children", [])
        in_list = rel.get("adopted_in", [])
        out_list = rel.get("adopted_out", [])
        
        for child in children:
            if child not in self.nodes:
                continue
            
            self._link_parent_child(p1, child)
            if p1 != p2:
                self._link_parent_child(p2, child)
            
            if child in in_list:
                self.nodes[child]["adopted_in"] = True
            if child in out_list:
                self.nodes[child]["adopted_out"] = True
    
    def _build_graph(self):
        for person in self.raw_ind:
            pid = person["id"]
            self.nodes[pid] = self._initialize_node(person)
        
        for rel in self.raw_rel:
            self._process_relationship(rel)
        
        for nid, node in self.nodes.items():
            gen = node["gen"]
            if gen not in self.generations:
                self.generations[gen] = []
            self.generations[gen].append(nid)
        
        for gen in self.generations:
            self.generations[gen].sort(key=lambda x: self.nodes[x]["sort_idx"])
    
    def _get_required_spacing(self, left_id, right_id):
        left_node = self.nodes[left_id]
        right_node = self.nodes[right_id]
        
        if right_id in left_node["spouse_ids"]:
            return self.PARTNER_SPACING
        
        left_parents = set(left_node["parent_ids"])
        right_parents = set(right_node["parent_ids"])
        
        if not left_parents and not right_parents:
            return self.MIN_SIB_SPACING + self.FAMILY_GAP
        
        if not left_parents.isdisjoint(right_parents):
            return self.MIN_SIB_SPACING
        
        return self.MIN_SIB_SPACING + self.FAMILY_GAP
    
    def _enforce_spacing(self, gen):
        nids = self.generations.get(gen, [])
        
        if len(nids) < 2:
            return
        
        for i in range(1, len(nids)):
            prev = nids[i-1]
            curr = nids[i]
            
            required_dist = self._get_required_spacing(prev, curr)
            min_x = self.nodes[prev]["x"] + self.NODE_WIDTH + required_dist
            
            if self.nodes[curr]["x"] < min_x - 0.001:
                shift = min_x - self.nodes[curr]["x"]
                for j in range(i, len(nids)):
                    self.nodes[nids[j]]["x"] += shift
    
    def _get_sibling_groups(self, gen):
        nids = self.generations.get(gen, [])
        groups = {}
        
        for nid in nids:
            p_tuple = tuple(sorted(self.nodes[nid]["parent_ids"]))
            if not p_tuple:
                continue
            
            if p_tuple not in groups:
                groups[p_tuple] = []
            groups[p_tuple].append(nid)
        
        return groups
    
    def _align_children_to_parents(self, gen):
        """Align children to be centered under their parents."""
        groups = self._get_sibling_groups(gen)
        
        for p_tuple, sib_ids in groups.items():
            # Calculate parent center
            # SPECIAL LOGIC: If a parent is a Surrogate ('S'), align to that parent explicitly.
            surrogate_parent = None
            for p in p_tuple:
                if self._is_surrogate(p):
                    surrogate_parent = p
                    break
            
            if surrogate_parent:
                center_parents = self.nodes[surrogate_parent]["x"]
            else:
                p_xs = [self.nodes[p]["x"] for p in p_tuple if p in self.nodes]
                if not p_xs:
                    continue
                center_parents = sum(p_xs) / len(p_xs)
            
            # Calculate sibling center
            sib_xs = [self.nodes[s]["x"] for s in sib_ids]
            center_sibs = (min(sib_xs) + max(sib_xs)) / 2
            
            # Shift siblings to align with parents
            shift = center_parents - center_sibs
            for sib in sib_ids:
                self.nodes[sib]["x"] += shift
    
    def _get_partner_group(self, nid, gen):
        node = self.nodes[nid]
        spouses = [
            s for s in node["spouse_ids"]
            if s in self.nodes and self.nodes[s]["gen"] == gen
        ]
        return [nid] + spouses
    
    def _align_parents_to_children(self, gen):
        nids = self.generations.get(gen, [])
        processed = set()
        
        for nid in nids:
            if nid in processed:
                continue
            
            node = self.nodes[nid]
            
            if not node["children_ids"]:
                continue
            
            group_ids = self._get_partner_group(nid, gen)
            
            all_children = set()
            for member_id in group_ids:
                all_children.update(self.nodes[member_id]["children_ids"])
            
            if not all_children:
                continue
            
            c_xs = [self.nodes[c]["x"] for c in all_children if c in self.nodes]
            if not c_xs:
                continue
            center_children = sum(c_xs) / len(c_xs)
            
            p_xs = [self.nodes[p]["x"] for p in group_ids]
            center_parents = (min(p_xs) + max(p_xs)) / 2
            
            shift = center_children - center_parents
            for parent in group_ids:
                self.nodes[parent]["x"] += shift
                processed.add(parent)
    
    def _initial_layout(self):
        for gen, nids in self.generations.items():
            current_x = 0.0
            
            for i, nid in enumerate(nids):
                if i > 0:
                    prev_nid = nids[i-1]
                    spacing = self._get_required_spacing(prev_nid, nid)
                    current_x += spacing + self.NODE_WIDTH
                
                self.nodes[nid]["x"] = current_x
    
    def _iterative_adjustment(self, iterations):
        for _ in range(iterations):
            for gen in sorted(self.generations.keys()):
                self._align_children_to_parents(gen)
                self._enforce_spacing(gen)
            
            for gen in sorted(self.generations.keys(), reverse=True):
                self._align_parents_to_children(gen)
                self._enforce_spacing(gen)
    
    def _final_priority_pass(self, priority):
        if priority == "Children to Parents (Top-down)":
            for gen in sorted(self.generations.keys()):
                self._align_children_to_parents(gen)
                self._enforce_spacing(gen)
        else:
            for gen in sorted(self.generations.keys(), reverse=True):
                self._align_parents_to_children(gen)
                self._enforce_spacing(gen)
    
    def _center_layout(self):
        all_x = [n["x"] for n in self.nodes.values()]
        
        if not all_x:
            return
        
        midpoint = (max(all_x) + min(all_x)) / 2
        
        for nid in self.nodes:
            self.nodes[nid]["x"] -= midpoint
    
    def calculate_layout(self, adjustment_iterations, priority="Children to Parents (Top-down)"):
        self._initial_layout()
        self._iterative_adjustment(adjustment_iterations)
        self._final_priority_pass(priority)
        self._center_layout()
        
        return self.nodes