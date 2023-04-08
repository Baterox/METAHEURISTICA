def forward_checking(domains, width, height, row_clues, col_clues, node_count, backtrack_count):
    selected_index = select_variable(domains)

    if selected_index == len(domains):
        return domains, node_count, backtrack_count

    node_count += 1

    for value in domains[selected_index]:
        assignment = {i: domains[i][0] for i in range(selected_index)}

        if is_consistent(assignment, selected_index, value, row_clues, col_clues, width, height):
            new_domains = [domain.copy() for domain in domains]
            new_domains[selected_index] = [value]

            for i in range(selected_index + 1, len(domains)):
                new_domains[i] = [v for v in domains[i] if is_consistent(assignment, i, v, row_clues, col_clues, width, height)]

            if all(new_domains[i] for i in range(selected_index + 1, len(domains))):
                result, new_node_count, new_backtrack_count = forward_checking(new_domains, width, height, row_clues, col_clues, node_count, backtrack_count)
                if result:
                    return result, new_node_count, new_backtrack_count
        else:
            backtrack_count += 1

    return None, node_count, backtrack_count