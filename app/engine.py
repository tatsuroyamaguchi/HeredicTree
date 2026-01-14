import copy

class PedigreeEngine:
    def __init__(self, data, config):
        self.raw_ind = data.get("individual", [])
        self.raw_rel = data.get("relationships", [])
        self.nodes = {} 
        self.generations = {}
        
        # Config
        self.GEN_HEIGHT = config['gen_height']
        self.NODE_WIDTH = config['node_width']
        self.MIN_SIB_SPACING = config['min_sib_spacing']
        self.PARTNER_SPACING = config['partner_spacing']
        self.FAMILY_GAP = config['family_gap']
        
        self._build_graph()

    def _is_donor(self, nid):
        """Check if a node is a donor based on 'affected' field."""
        if nid not in self.nodes: return False
        raw = self.nodes[nid]["data"].get("affected", "")
        vals = []
        if isinstance(raw, list):
            vals = [str(x).strip() for x in raw]
        else:
            # Handle string input like "D, A" or "D;A"
            norm = str(raw).replace(",", ";").replace(" ", ";")
            vals = [x.strip() for x in norm.split(";") if x.strip()]
        return "D" in vals

    def _build_graph(self):
        """Build nodes."""
        # 1. Initialize nodes
        for p in self.raw_ind:
            pid = p["id"]
            gen = self._parse_gen(pid)
            
            self.nodes[pid] = {
                "data": p,
                "id": pid,
                "gen": gen,
                "spouse_ids": [],
                "children_ids": [], 
                "parent_ids": [],
                "adopted_in": False, 
                "adopted_out": False,
                "x": 0.0,
                "y": - (gen * self.GEN_HEIGHT),
                "width_val": self.NODE_WIDTH,
                "sort_idx": self._parse_individual_number(pid)
            }

        # 2. Build relationships
        for r in self.raw_rel:
            p1 = r.get("p1")
            p2 = r.get("p2")
            if not p1 or p1 not in self.nodes: continue
            if not p2: p2 = p1
            if p2 not in self.nodes: p2 = p1
            
            children = r.get("children", [])
            in_list = r.get("adopted_in", [])
            out_list = r.get("adopted_out", [])
            
            # Check donor status
            is_p1_donor = self._is_donor(p1)
            is_p2_donor = self._is_donor(p2)
            
            # Register partners
            # Donors are excluded from spouse linking to prevent forced spacing/grouping
            if p1 in self.nodes and p2 in self.nodes and p1 != p2:
                if not is_p1_donor and not is_p2_donor:
                    if p2 not in self.nodes[p1]["spouse_ids"]: 
                        self.nodes[p1]["spouse_ids"].append(p2)
                    if p1 not in self.nodes[p2]["spouse_ids"]: 
                        self.nodes[p2]["spouse_ids"].append(p1)
            
            # Register parent-child
            # Donors are excluded from parent-child linking to prevent layout alignment
            for c in children:
                if c in self.nodes:
                    # Link p1 if not donor
                    if p1 in self.nodes:
                        if not is_p1_donor:
                            self.nodes[c]["parent_ids"].append(p1)
                            if c not in self.nodes[p1]["children_ids"]: 
                                self.nodes[p1]["children_ids"].append(c)
                    
                    # Link p2 if not donor (and distinct)
                    if p2 in self.nodes and p1 != p2:
                        if not is_p2_donor:
                            self.nodes[c]["parent_ids"].append(p2)
                            if c not in self.nodes[p2]["children_ids"]: 
                                self.nodes[p2]["children_ids"].append(c)
                    
                    if c in in_list:
                        self.nodes[c]["adopted_in"] = True
                    if c in out_list:
                        self.nodes[c]["adopted_out"] = True

        # 3. Group by generation
        for nid, node in self.nodes.items():
            g = node["gen"]
            if g not in self.generations: 
                self.generations[g] = []
            self.generations[g].append(nid)
            
        for g in self.generations:
            self.generations[g].sort(key=lambda x: self.nodes[x]["sort_idx"])

    def _parse_gen(self, pid):
        prefix = pid.split("-")[0]
        romans = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
                  "XI": 1, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15}
        return romans.get(prefix, 1)

    def _parse_individual_number(self, pid):
        try:
            return int(pid.split("-")[-1])
        except:
            return 9999 

    def calculate_layout(self, adjustment_iterations, priority="Children to Parents (Top-down)"):
        # Phase 1: Initial (Left packed)
        for g, nids in self.generations.items():
            current_x = 0.0
            for i, nid in enumerate(nids):
                if i > 0:
                    prev_nid = nids[i-1]
                    spacing = self._get_required_spacing(prev_nid, nid)
                    current_x += spacing + self.NODE_WIDTH
                self.nodes[nid]["x"] = current_x

        # Phase 2: Adjustment
        for i in range(adjustment_iterations):
            for g in sorted(self.generations.keys()):
                self._align_children_to_parents(g)
                self._enforce_spacing(g)
            
            for g in sorted(self.generations.keys(), reverse=True):
                self._align_parents_to_children(g)
                self._enforce_spacing(g)

        if priority == "Children to Parents (Top-down)":
            for g in sorted(self.generations.keys()):
                self._align_children_to_parents(g)
                self._enforce_spacing(g)
        else:
            for g in sorted(self.generations.keys(), reverse=True):
                self._align_parents_to_children(g)
                self._enforce_spacing(g)

        # Center
        all_x = [n["x"] for n in self.nodes.values()]
        if all_x:
            midpoint = (max(all_x) + min(all_x)) / 2
            for nid in self.nodes:
                self.nodes[nid]["x"] -= midpoint
                
        return self.nodes

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
        if len(nids) < 2: return

        for i in range(1, len(nids)):
            prev = nids[i-1]
            curr = nids[i]
            
            required_dist = self._get_required_spacing(prev, curr)
            min_x = self.nodes[prev]["x"] + self.NODE_WIDTH + required_dist
            
            if self.nodes[curr]["x"] < min_x - 0.001:
                shift = min_x - self.nodes[curr]["x"]
                for j in range(i, len(nids)):
                    self.nodes[nids[j]]["x"] += shift

    def _align_children_to_parents(self, gen):
        nids = self.generations.get(gen, [])
        groups = {}
        for nid in nids:
            p_tuple = tuple(sorted(self.nodes[nid]["parent_ids"]))
            if not p_tuple: continue
            if p_tuple not in groups: groups[p_tuple] = []
            groups[p_tuple].append(nid)

        for p_tuple, sib_ids in groups.items():
            p_xs = [self.nodes[p]["x"] for p in p_tuple if p in self.nodes]
            if not p_xs: continue
            center_parents = sum(p_xs) / len(p_xs)
            
            sib_xs = [self.nodes[s]["x"] for s in sib_ids]
            center_sibs = (min(sib_xs) + max(sib_xs)) / 2
            
            shift = center_parents - center_sibs
            for s in sib_ids:
                self.nodes[s]["x"] += shift

    def _align_parents_to_children(self, gen):
        nids = self.generations.get(gen, [])
        processed = set()

        for nid in nids:
            if nid in processed: continue
            
            node = self.nodes[nid]
            children = node["children_ids"]
            
            if not children: continue

            spouses = [s for s in node["spouse_ids"] if s in self.nodes and self.nodes[s]["gen"] == gen]
            group_ids = [nid] + spouses
            
            all_children = set()
            for member_id in group_ids:
                all_children.update(self.nodes[member_id]["children_ids"])
            
            if not all_children: continue

            c_xs = [self.nodes[c]["x"] for c in all_children if c in self.nodes]
            if not c_xs: continue
            center_children = sum(c_xs) / len(c_xs)

            p_xs = [self.nodes[p]["x"] for p in group_ids]
            center_parents = (min(p_xs) + max(p_xs)) / 2

            shift = center_children - center_parents

            for p in group_ids:
                self.nodes[p]["x"] += shift
                processed.add(p)