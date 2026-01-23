import json

from parameter import DEFAULT_LAYOUT, GENERATION_LABELS


def parse_input_string(s):
    """
    Parse comma-separated string into list.
    Example: 'M, F' -> ['M', 'F']
    Handles both full-width and half-width commas.
    """
    s = s.replace("、", ",")  # Convert full-width comma
    return [x.strip() for x in s.split(",") if x.strip()]


def create_grandparents():
    """Create grandparent individuals."""
    grandparents = []
    
    for i in range(1, 5):
        grandparents.append({
            "id": f"I-{i}",
            "gender": "M" if i % 2 == 1 else "F",
            "label": GENERATION_LABELS[i]
        })
    
    return grandparents


def create_generation_two(paternal_sibs, maternal_sibs, father_idx, mother_idx):
    """
    Create second generation (parents and their siblings).
    
    Returns:
        tuple: (individuals_list, paternal_children_ids, maternal_children_ids, 
                father_id, mother_id)
    """
    gen2_genders = paternal_sibs + maternal_sibs
    individuals = []
    paternal_children = []
    maternal_children = []
    
    # Adjust indices to 0-based
    f_idx = father_idx - 1
    m_idx = mother_idx - 1
    
    for i, gender in enumerate(gen2_genders):
        ind_id = f"II-{i+1}"
        
        # Determine label
        label = ""
        if i == f_idx:
            label = "Father"
        elif i == m_idx:
            label = "Mother"
        
        # Create individual
        individuals.append({
            "id": ind_id,
            "gender": gender,
            "label": label,
            "affected": "",
            "deceased": "",
            "proband": "",
            "client": "",
            "documented": "",
            "pregnancy": ""
        })
        
        # Categorize by family
        if i < len(paternal_sibs):
            paternal_children.append(ind_id)
        else:
            maternal_children.append(ind_id)
    
    father_id = f"II-{father_idx}"
    mother_id = f"II-{mother_idx}"
    
    return individuals, paternal_children, maternal_children, father_id, mother_id


def create_generation_three(my_sibs, self_idx):
    """
    Create third generation (self and siblings).
    
    Returns:
        list: List of individual dictionaries
    """
    individuals = []
    s_idx = self_idx - 1  # Convert to 0-based
    
    for i, gender in enumerate(my_sibs):
        ind_id = f"III-{i+1}"
        is_self = (i == s_idx)
        
        individuals.append({
            "id": ind_id,
            "gender": gender,
            "label": "Self" if is_self else "",
            "proband": is_self,
            "client": is_self,
            "affected": "",
            "deceased": "",
            "documented": "",
            "pregnancy": ""
        })
    
    return individuals


def create_grandparent_relationships(paternal_children, maternal_children):
    """Create relationships for grandparents to their children."""
    relationships = []
    
    # Paternal grandparents
    if paternal_children:
        relationships.append({
            "p1": "I-1",
            "p2": "I-2",
            "children": paternal_children,
            "divorced": "",
            "multiples": [],
            "adopted_in": [],
            "adopted_out": [],
            "consanguinity": ""
        })
    
    # Maternal grandparents
    if maternal_children:
        relationships.append({
            "p1": "I-3",
            "p2": "I-4",
            "children": maternal_children,
            "divorced": "",
            "multiples": [],
            "adopted_in": [],
            "adopted_out": [],
            "consanguinity": ""
        })
    
    return relationships


def create_parent_relationship(father_id, mother_id, gen3_ids):
    """Create relationship between parents and their children."""
    if not father_id or not mother_id:
        return None
    
    return {
        "p1": father_id,
        "p2": mother_id,
        "children": gen3_ids,
        "divorced": "",
        "multiples": [],
        "adopted_in": [],
        "adopted_out": [],
        "consanguinity": ""
    }


def generate_pedigree_data(paternal_sibs, maternal_sibs, father_idx, 
                          mother_idx, my_sibs, self_idx):
    """
    Generate HeredicTree JSON data from input parameters.
    
    Args:
        paternal_sibs: List of paternal sibling genders
        maternal_sibs: List of maternal sibling genders
        father_idx: 1-based index of father in combined sibling list
        mother_idx: 1-based index of mother in combined sibling list
        my_sibs: List of sibling genders in self's generation
        self_idx: 1-based index of self in sibling list
    
    Returns:
        dict: Complete pedigree JSON structure
    """
    # Generate individuals by generation
    gen1_individuals = create_grandparents()
    
    gen2_individuals, paternal_children, maternal_children, father_id, mother_id = \
        create_generation_two(paternal_sibs, maternal_sibs, father_idx, mother_idx)
    
    gen3_individuals = create_generation_three(my_sibs, self_idx)
    gen3_ids = [ind["id"] for ind in gen3_individuals]
    
    # Combine all individuals
    all_individuals = gen1_individuals + gen2_individuals + gen3_individuals
    
    # Generate relationships
    relationships = create_grandparent_relationships(paternal_children, maternal_children)
    
    parent_rel = create_parent_relationship(father_id, mother_id, gen3_ids)
    if parent_rel:
        relationships.append(parent_rel)
    
    # Build complete JSON structure
    return {
        "meta": {"comments": "Generated by Streamlit App"},
        "layout": DEFAULT_LAYOUT,
        "individual": all_individuals,
        "relationships": relationships
    }