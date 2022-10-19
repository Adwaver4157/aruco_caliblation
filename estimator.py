def convert_oracle_to_image_pos(image_pos_dict, target_oracle_pos=[8, 6], table_size=[15, 15]):
    cornerUL = image_pos_dict[0]
    cornerDR = image_pos_dict[3]
    diff = cornerDR - cornerUL
    target_image_pos = target_oracle_pos * (diff / table_size) + cornerUL
    target_pos_int = [int(x) for x in target_image_pos]
    print(diff)
    print(target_pos_int)
    # target_image_pos = [100, 100]
    return target_pos_int

def convert_image_to_table_pos(image_pos_dict, table_pos_dict, target_image_pos, table_size=[15, 15]):
    cornerUL = image_pos_dict[0]
    cornerDR = image_pos_dict[3]
    diff = cornerDR - cornerUL
    target_table_pos = target_image_pos * (table_size / diff)
    # target_table_pos = [8, 6]
    return target_table_pos