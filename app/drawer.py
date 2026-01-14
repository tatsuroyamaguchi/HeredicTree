import copy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon, Rectangle


def get_affected_list(node_data):
    """
    affectedデータを安全にリスト形式に変換・解析するヘルパー関数
    文字列 "D", "A, D" や リスト ["D", "A"] などを統一的に処理
    """
    raw = node_data.get("affected", [])
    if raw is None:
        return []
    if isinstance(raw, list):
        # 既にリストの場合は文字列化して返す
        return [str(x).strip() for x in raw if str(x).strip()]
    if isinstance(raw, str):
        # 文字列の場合はカンマやセミコロンで分割
        normalized = raw.replace(",", ";").replace(" ", ";")
        return [code.strip() for code in normalized.split(";") if code.strip()]
    # 数値(NaN含む)などの場合
    if str(raw).lower() != 'nan':
         return [str(raw).strip()]
    return []


def draw_symbol(ax, x, y, engine_node, config, display_number=None):
    """Draw individual symbol."""
    node_data = engine_node["data"]
    is_adopted_in = engine_node.get("adopted_in", False)
    is_adopted_out = engine_node.get("adopted_out", False)
    is_any_adopted = is_adopted_in or is_adopted_out
    
    gender = node_data.get("gender", "N")
    affected_list = get_affected_list(node_data)
    
    # --- Check for Donor status ---
    is_donor = "D" in affected_list
    # Remove "D" from affected list for fill logic so it doesn't turn black automatically
    # unless "A" is also explicitly present (though typically D is open)
    fill_candidates = [a for a in affected_list if a != "D"]
    
    deceased = node_data.get("deceased", False)
    proband = node_data.get("proband", False)
    client = node_data.get("client", False)
    documented = node_data.get("documented", False)
    label = node_data.get("label", "")
    pregnancy = node_data.get("pregnancy", "")
    
    size = config['symbol_size']
    lw = config['line_width']
    fsize = config['font_size']
    label_offset = config['label_offset']
    
    hs = size / 2 
    
    # 2. Base Shape
    patch = None
    if gender == "M":
        patch = Rectangle((x - hs, y - hs), size, size, edgecolor='black', facecolor='white', lw=lw, zorder=10)
    elif gender == "F":
        patch = Circle((x, y), hs, edgecolor='black', facecolor='white', lw=lw, zorder=10)
    elif gender == "A":
        patch = Polygon([[x - hs, y - hs/2], [x, y + hs], [x + hs, y - hs/2]], closed=True, edgecolor='black', facecolor='white', lw=lw, zorder=10)
    elif gender in ["N", "U", "non-binary"]:
        patch = Polygon([[x, y+hs], [x+hs, y], [x, y-hs], [x-hs, y]], closed=True, edgecolor='black', facecolor='white', lw=lw, zorder=10)
    elif gender == "I":
        pass 
    elif gender == "NC":
        pass 
        
    # Multiple individuals handling
    elif isinstance(gender, str) and len(gender) > 1:
        if gender.startswith("M") and gender[1:].isdigit():
            patch = Rectangle((x - hs, y - hs), size, size, edgecolor='black', facecolor='white', lw=lw, zorder=10)
            ax.text(x, y, gender[1:], ha="center", va="center", fontsize=fsize*1.2, zorder=11)
        elif gender.startswith("F") and gender[1:].isdigit():
            patch = Circle((x, y), hs, edgecolor='black', facecolor='white', lw=lw, zorder=10)
            ax.text(x, y, gender[1:], ha="center", va="center", fontsize=fsize*1.2, zorder=11)
        elif gender.startswith("N") and gender[1:]:
            patch = Polygon([[x, y+hs], [x+hs, y], [x, y-hs], [x-hs, y]], closed=True, edgecolor='black', facecolor='white', lw=lw, zorder=10)
            ax.text(x, y, gender[1:], ha="center", va="center", fontsize=fsize*1.2, zorder=11)
        
    if patch:
        ax.add_patch(patch)

        # 3. Fill Logic
        if "A" in affected_list:
            patch.set_facecolor('black')
        else:
            patch.set_facecolor('white')
            
            def add_overlay(patch, ax, clip_rect, color, zorder=11):
                overlay = copy.copy(patch)
                overlay.set_facecolor(color)
                overlay.set_edgecolor('black')
                overlay.set_zorder(zorder)
                overlay.set_clip_path(clip_rect.get_path(), clip_rect.get_transform())
                ax.add_patch(overlay)

            if "A2-1" in affected_list:
                clip_rect = Rectangle((x, y - hs), hs, size, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='black')
            if "A2-2" in affected_list:
                clip_rect = Rectangle((x - hs, y - hs), hs, size, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='#999999')
            if "A4-1" in affected_list:
                clip_rect = Rectangle((x, y), hs, hs, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='black')
            if "A4-2" in affected_list:
                clip_rect = Rectangle((x, y - hs), hs, hs, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='#444444')
            if "A4-3" in affected_list:
                clip_rect = Rectangle((x - hs, y - hs), hs, hs, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='#999999')
            if "A4-4" in affected_list:
                clip_rect = Rectangle((x - hs, y), hs, hs, transform=ax.transData)
                add_overlay(patch, ax, clip_rect, color='#CCCCCC')
        
        if "C" in affected_list:
            ax.add_line(Line2D([x, x], [y-hs*0.9, y+hs*0.9], color='black', lw=lw, zorder=11))
        
    # 4. Other Indicators
    if is_donor:
        # Determine text color based on fill
        text_color = 'white' if "A" in fill_candidates else 'black'
        ax.text(x, y, "D", ha="center", va="center", color=text_color, fontsize=fsize * 1.2, fontweight='normal', zorder=20)
        
    if deceased:
        ax.add_line(Line2D([x-hs-0.1, x+hs+0.1], [y-hs-0.1, y+hs+0.1], color='black', lw=lw, zorder=12))

    if gender == "I":
        ax.add_line(Line2D([x-hs, x+hs], [y+0.4, y+0.4], color='black', lw=lw))
        ax.add_line(Line2D([x-hs, x+hs], [y+0.2, y+0.2], color='black', lw=lw))
    elif gender == "NC":
        ax.add_line(Line2D([x-hs, x+hs], [y+0.4, y+0.4], color='black', lw=lw))

    if proband:
        ax.annotate("P", xy=(x - hs, y), xytext=(x - hs - 1, y - 0.4), 
                    color='black', fontsize=fsize*1.2, zorder=15)
        
    if client:
        scale_factor = fsize / 12.0
        arrow_dist = 0.75 * scale_factor
        ax.annotate("", xy=(x - hs, y), 
                    xytext=(x - hs - arrow_dist, y - arrow_dist),
                    arrowprops=dict(arrowstyle="->", color='black', lw=lw, mutation_scale=fsize), 
                    zorder=15)

    if documented:
        # シンボルの右下に"*"を表示
        ax.text(x + hs + 0.15, y - hs*1.5, "*", 
                ha="left", va="bottom", fontsize=fsize * 2, color='black', zorder=15)
    
    if label:
        wrapped_label = "\n".join([label[i:i+15] for i in range(0, len(label), 15)]) if "\n" not in label else label
        ax.text(x, y - hs - label_offset, wrapped_label, 
                ha="center", va="top", fontsize=fsize, 
                linespacing=1.2,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1), zorder=20)

    num_str = ""
    if display_number:
        num_str = str(display_number)
    elif 'id' in node_data:
        try:
            num_str = node_data['id'].split('-')[-1]
        except: pass
    
    if num_str:
        ax.text(x + hs + 0.15, y + hs - 0.25, num_str, 
                ha="left", va="bottom", fontsize=fsize, zorder=12)
    
    if pregnancy is True or str(pregnancy).upper() == "P":
        p_color = 'white' if "A" in affected_list else 'black'
        ax.text(x, y, "P", ha="center", va="center", 
                color=p_color, fontsize=fsize * 1.2, fontweight='bold', zorder=20) 
    
    if is_any_adopted:
        pad = 0.2
        bracket_w = 0.15
        ax.add_line(Line2D([x - hs - pad, x - hs - pad], [y + hs + pad, y - hs - pad], color='black', lw=lw, zorder=13))
        ax.add_line(Line2D([x - hs - pad, x - hs - pad + bracket_w], [y + hs + pad, y + hs + pad], color='black', lw=lw, zorder=13))
        ax.add_line(Line2D([x - hs - pad, x - hs - pad + bracket_w], [y - hs - pad, y - hs - pad], color='black', lw=lw, zorder=13))
        
        ax.add_line(Line2D([x + hs + pad, x + hs + pad], [y + hs + pad, y - hs - pad], color='black', lw=lw, zorder=13))
        ax.add_line(Line2D([x + hs + pad, x + hs + pad - bracket_w], [y + hs + pad, y + hs + pad], color='black', lw=lw, zorder=13))
        ax.add_line(Line2D([x + hs + pad, x + hs + pad - bracket_w], [y - hs - pad, y - hs - pad], color='black', lw=lw, zorder=13))

def draw_pedigree_chart(engine_nodes, relationships, config, meta=None):
    """Draw complete pedigree chart"""
    gen_height = config['gen_height']
    lw = config['line_width']
    u_shape_offset = config['u_shape_offset']
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_aspect('equal')
    ax.axis('off')
    
    def get_pos(nid):
        if nid in engine_nodes:
            return engine_nodes[nid]["x"], engine_nodes[nid]["y"]
        return None, None

    def check_is_donor(nid):
        if nid not in engine_nodes: return False
        aff_list = get_affected_list(engine_nodes[nid]["data"])
        return "D" in aff_list
    
    connection_levels = {}

    for r in relationships:
        p1 = r.get("p1")
        p2 = r.get("p2")
        children = r.get("children", [])
        in_list = r.get("adopted_in", [])
        div_status = r.get("divorced", "")
        is_consanguineous = r.get("consanguinity", False)
        multiples = r.get("multiples", [])
        
        if not p1: continue
        
        # --- ドナー判定 ---
        p1_is_donor = check_is_donor(p1)
        p2_is_donor = check_is_donor(p2) if p2 else False
        
        valid_children = [c for c in children if c in engine_nodes]

        # ドナーの子供のIDを取得
        donor_children = []
        if p1_is_donor:
            donor_children.extend(valid_children)
        if p2_is_donor:
            donor_children.extend(valid_children)
        donor_children = list(set(donor_children))
        
        # donor_childrenがvalid_childrenに含まれる親のIDを取得
        non_donor_parents = []
        for c in donor_children:
            for r_check in relationships:
                if c in r_check.get("children", []):
                    p1_check = r_check.get("p1")
                    p2_check = r_check.get("p2")
                    if p1_check and not check_is_donor(p1_check):
                        non_donor_parents.append(p1_check)
                    if p2_check and not check_is_donor(p2_check):
                        non_donor_parents.append(p2_check)
        non_donor_parents = list(set(non_donor_parents))
        
        # non_donor_parentsの子供の数を取得
        num_siblings = {}
        for p in non_donor_parents:
            count = 0
            for r_check in relationships:
                if p == r_check.get("p1") or p == r_check.get("p2"):
                    count += len([c for c in r_check.get("children", []) if c in engine_nodes])
            num_siblings[p] = count
            
        # --- ドナー接続線の描画 (直線) ---
        # 親がドナーの場合、親から子供たちへ直線を引く
        if (p1_is_donor and valid_children) or (p2_is_donor and valid_children):
            x_d, y_d = get_pos(p1)
            for cid in valid_children:
                xc, yc = get_pos(cid)
                try:
                    is_single_child = (count == 1)
                except NameError:
                    is_single_child = True

                if is_single_child:
                    # シンボルの中心(x_d, y_d) から 子供のシンボルの上縁へ直線を引く
                    ax.add_line(Line2D([x_d, xc], [y_d, yc+config['symbol_size'] / 2], color='black', lw=lw, zorder=5))
                else:
                    # sibship lineの高さからドナーのシンボルに直線を引く
                    c_gen = min([engine_nodes[c]["gen"] for c in valid_children], default=gen1+1)
                    child_y_level = - (c_gen * gen_height)
                    sibship_y = child_y_level + (gen_height * 0.3) 
                    ax.add_line(Line2D([x_d, xc], [y_d, sibship_y], color='black', lw=lw, zorder=5))

        # --- 通常のカギ型配線の準備 ---
        # ドナーである親は、通常のカギ型配線ロジック上の「親」としては扱わない（Noneにする）
        # これにより、ドナー側からのカギ型線が描画されるのを防ぐ
        eff_p1 = p1 if not p1_is_donor else None
        eff_p2 = p2 if (p2 and not p2_is_donor) else None
        
        # 両親ともドナー、あるいは片親のみでその人がドナーだった場合 -> 通常描画は不要
        if eff_p1 is None and eff_p2 is None:
            continue
            
        # 片方がドナーで、もう片方が通常親の場合（例: 母 + 精子ドナー）
        # 通常親（母）については、通常の「親1人の場合の描画ロジック」を適用して子供と繋ぐ必要がある
        if eff_p1 is None and eff_p2 is not None:
            # ドナーでない方をp1として扱う（シングルペアレント的な処理に持ち込む）
            eff_p1 = eff_p2
            eff_p2 = eff_p2 
        elif eff_p1 is not None and eff_p2 is None:
            # p2がドナーだった場合、p1だけで処理
            eff_p2 = eff_p1
            
        # --- ここから通常の配線ロジック (ドナーは除外済み) ---
        p1_curr = eff_p1
        p2_curr = eff_p2
        
        if p1_curr not in engine_nodes: continue
        
        x1, y1 = get_pos(p1_curr)
        x2, y2 = get_pos(p2_curr)
        
        gen1 = engine_nodes[p1_curr]["gen"]
        gen2 = engine_nodes[p2_curr]["gen"]
        
        mid_x = 0 
        line_y = 0 
        rel_min_x, rel_max_x = x1, x1

        # パートナー線 (水平線)
        if p1_curr == p2_curr:
            # シングル（またはパートナーがドナーで除外された）ケース
            # 親から少し下に線を下ろす
            mid_x = x1
            line_y = y1 - 0.5
            ax.add_line(Line2D([x1, x1], [y1, line_y], color='black', lw=lw, zorder=1))
            rel_min_x, rel_max_x = x1, x1

        elif gen1 == gen2:
            line_y = y1 
            left_x, right_x = min(x1, x2), max(x1, x2)
            rel_min_x, rel_max_x = left_x, right_x
            mid_x = (x1 + x2) / 2
            
            others_between = [
                nid for nid, n in engine_nodes.items() 
                if n["gen"] == gen1 
                and left_x < n["x"] < right_x
                and nid != p1_curr and nid != p2_curr
            ]
            
            if others_between:
                gen_key = engine_nodes[p1_curr]["gen"]
                level = connection_levels.get(gen_key, 0)
                connection_levels[gen_key] = level + 1
                
                current_u_offset = u_shape_offset + (level * 0.5)
                bottom_y = y1 - current_u_offset
                
                if is_consanguineous:
                    offset = 0.15
                    ax.add_line(Line2D([x1-offset, x1-offset], [y1, bottom_y+offset], color='black', lw=lw))
                    ax.add_line(Line2D([x1+offset, x1+offset], [y1, bottom_y-offset], color='black', lw=lw))
                    ax.add_line(Line2D([x2-offset, x2-offset], [y2, bottom_y+offset], color='black', lw=lw))
                    ax.add_line(Line2D([x2+offset, x2+offset], [y2, bottom_y-offset], color='black', lw=lw))
                    ax.add_line(Line2D([x1, x2], [bottom_y+offset, bottom_y+offset], color='black', lw=lw))
                    ax.add_line(Line2D([x1, x2], [bottom_y-offset, bottom_y-offset], color='black', lw=lw))
                else:
                    ax.add_line(Line2D([x1, x1], [y1, bottom_y], color='black', lw=lw))
                    ax.add_line(Line2D([x2, x2], [y2, bottom_y], color='black', lw=lw))
                    ax.add_line(Line2D([x1, x2], [bottom_y, bottom_y], color='black', lw=lw))
                line_y = bottom_y
            else:
                if is_consanguineous:
                    offset = 0.1
                    ax.add_line(Line2D([x1, x2], [line_y + offset, line_y + offset], color='black', lw=lw))
                    ax.add_line(Line2D([x1, x2], [line_y - offset, line_y - offset], color='black', lw=lw))
                else:
                    ax.add_line(Line2D([x1, x2], [line_y, line_y], color='black', lw=lw))

            if str(div_status).startswith("D"):
                slash_x = mid_x
                if div_status == "D_p1": slash_x = x1 + (x2 - x1) * 0.4
                if div_status == "D_p2": slash_x = x1 + (x2 - x1) * 0.6
                s_size = 0.3
                d_gap = 0.15
                ax.add_line(Line2D([slash_x - d_gap - s_size, slash_x - d_gap + s_size], [line_y - s_size*1.5, line_y + s_size*1.5], color='black', lw=lw))
                ax.add_line(Line2D([slash_x + d_gap - s_size, slash_x + d_gap + s_size], [line_y - s_size*1.5, line_y + s_size*1.5], color='black', lw=lw))

        else:
            # Inter-generational
            if gen1 < gen2:
                x_up, y_up = x1, y1
                x_low, y_low = x2, y2
            else:
                x_up, y_up = x2, y2
                x_low, y_low = x1, y1
            
            line_y = y_low 
            hs = config['symbol_size'] / 2
            offset = 0.1
            
            if x_up < x_low: stop_x = x_low - hs
            else: stop_x = x_low + hs

            rel_min_x, rel_max_x = min(x_up, stop_x), max(x_up, stop_x)

            if is_consanguineous:
                ax.add_line(Line2D([x_up - offset, x_up - offset], [y_up, line_y + offset], color='black', lw=lw))
                ax.add_line(Line2D([x_up + offset, x_up + offset], [y_up, line_y - offset], color='black', lw=lw))
                ax.add_line(Line2D([x_up, stop_x], [line_y + offset, line_y + offset], color='black', lw=lw))
                ax.add_line(Line2D([x_up, stop_x], [line_y - offset, line_y - offset], color='black', lw=lw))
            else:
                ax.add_line(Line2D([x_up, x_up], [y_up, line_y], color='black', lw=lw))
                ax.add_line(Line2D([x_up, stop_x], [line_y, line_y], color='black', lw=lw))

            if str(div_status).startswith("D"):
                slash_x = (x_up + stop_x) / 2
                s_size = 0.3
                d_gap = 0.15
                ax.add_line(Line2D([slash_x - d_gap - s_size, slash_x - d_gap + s_size], [line_y - s_size*1.5, line_y + s_size*1.5], color='black', lw=lw))
                ax.add_line(Line2D([slash_x + d_gap - s_size, slash_x + d_gap + s_size], [line_y - s_size*1.5, line_y + s_size*1.5], color='black', lw=lw))
            pass
            mid_x = (x_up + stop_x) / 2

        # --- Children Connections ---
        if valid_children:
            c_gen = min([engine_nodes[c]["gen"] for c in valid_children], default=gen1+1)
            child_y_level = - (c_gen * gen_height)
            sibship_y = child_y_level + (gen_height * 0.3) 
            
            # シングル親(ドナーパートナー含む)の場合、子供が真下にいれば線を真っ直ぐにする調整
            if len(valid_children) == 1:
                child_id = valid_children[0]
                cx, cy = get_pos(child_id)
                if p1_curr == p2_curr: # シングル扱い
                    tolerance = 0.1
                    if rel_min_x - tolerance <= cx <= rel_max_x + tolerance:
                        mid_x = cx

            # 多胎児計算など
            mult_map = {}
            for m in multiples:
                ids = tuple(sorted(m.get("ids", [])))
                mult_map[ids] = m.get("type", "dizygotic")
            
            connection_xs = []
            processed_in_mult = set()
            for m_ids in mult_map.keys():
                m_xs = [engine_nodes[cid]["x"] for cid in m_ids if cid in engine_nodes]
                if m_xs:
                    connection_xs.append(sum(m_xs) / len(m_xs))
                    processed_in_mult.update(m_ids)
            for cid in valid_children:
                if cid not in processed_in_mult:
                    connection_xs.append(engine_nodes[cid]["x"])

            if connection_xs:
                min_cx = min(connection_xs)
                max_cx = max(connection_xs)
                
                # 親からの垂直線
                ax.add_line(Line2D([mid_x, mid_x], [line_y, sibship_y], color='black', lw=lw))

                # 兄弟姉妹を結ぶ水平バー
                bar_min = min(min_cx, mid_x)
                bar_max = max(max_cx, mid_x)
                if bar_max > bar_min + 1e-5:
                    ax.add_line(Line2D([bar_min, bar_max], [sibship_y, sibship_y], color='black', lw=lw))

            processed_children = set()
            
            # Multiple births
            for m_ids, m_type in mult_map.items():
                m_points = []
                for cid in m_ids:
                    if cid in engine_nodes:
                        m_points.append(get_pos(cid))
                        processed_children.add(cid)
                if not m_points: continue
                
                m_xs = [p[0] for p in m_points]
                apex_x = sum(m_xs) / len(m_xs)
                apex_y = sibship_y
                
                for cx, cy in m_points:
                    ax.add_line(Line2D([apex_x, cx], [apex_y, cy + config['symbol_size']/2], color='black', lw=lw, zorder=1))
                
                if m_type == "monozygotic":
                    bar_y = apex_y - (gen_height * 0.1)
                    w = (max(m_xs) - min(m_xs)) / 2 * 0.5
                    ax.add_line(Line2D([apex_x - w, apex_x + w], [bar_y, bar_y], color='black', lw=lw))
                elif m_type == "unknown":
                    ax.text(apex_x, apex_y - 0.5, "?", ha="center", va="top", fontsize=config['font_size']*1.5, zorder=20)

            # Regular children
            for cid in valid_children:
                if cid in processed_children: continue
                # 多胎児処理済みなどはスキップ
                is_mult = False
                for m_ids in mult_map:
                    if cid in m_ids: is_mult = True
                if is_mult: continue

                cx, cy = get_pos(cid)
                ls = '--' if cid in in_list else '-'
                
                # ここが重要: 通常親からの線を描く
                ax.add_line(Line2D([cx, cx], [sibship_y, cy + config['symbol_size']/2], 
                                color='black', lw=lw, linestyle=ls, zorder=1))

    # Draw Nodes
    for nid, node in engine_nodes.items():
        draw_symbol(ax, node["x"], node["y"], node, config, display_number=None)

    # Labels & Meta
    all_x = [n["x"] for n in engine_nodes.values()]
    all_y = [n["y"] for n in engine_nodes.values()]
    
    if all_x:
        min_x = min(all_x) - 3.0
        romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}
        present_gens = sorted(list(set(n["gen"] for n in engine_nodes.values())))
        for g in present_gens:
            y_coord = - (g * gen_height)
            label = romans.get(g, str(g))
            ax.text(min_x, y_coord, label, fontsize=config['font_size'] * 1.5, fontweight='bold', va='center', ha='center')

    if meta:
        comment_text = meta.get("comments", "")
        if comment_text:
            ax.text(0.99, 0.04, comment_text, transform=ax.transAxes, ha='right', va='bottom', fontsize=config['font_size'])

    if all_x and all_y:
        margin = 3.0
        ax.set_xlim(min(all_x) - margin - 1, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin - 3, max(all_y) + margin)

    return fig