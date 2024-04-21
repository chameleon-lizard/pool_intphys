import json
import pathlib


def replace_id_with_number(line: str, id_table: dict):
    line = json.loads(line)
    line['id'] = id_table[line['id']]
    return json.dumps(line)


def check_if_speeds_are_zero(line: str):
    line = json.loads(line)

    return line['velocity_x'] == line['velocity_y'] == 0


def clean_data(input_path: str, output_path: str):
    txt = '\n'.join(pathlib.Path(input_path).read_text().splitlines()[2:])

    blocks = txt.split('\n\n')

    ids = {json.loads(line)['id'] for line in blocks[0].splitlines()}
    ids = {key: value for value, key in enumerate(ids)}

    turns = {json.loads(line)['turn_number'] for line in '\n'.join(blocks).splitlines()}

    turn_dict = {
        key: [] for key in turns
    }
    print(turns)
    
    blocks_clean = []
    for block in blocks:
        if not all(check_if_speeds_are_zero(line) for line in block.splitlines()):
            blocks_clean.append(block)

    txt = '\n'.join(blocks_clean)

    for block in blocks_clean:
        key = json.loads(block.splitlines()[0])['turn_number']
        turn_dict[key].append([replace_id_with_number(line, ids) for line in block.splitlines()])

    txt = [replace_id_with_number(line, ids) for line in txt.splitlines()]

    pathlib.Path(output_path).write_text(json.dumps(turn_dict, indent=4))


if __name__ == '__main__':
    input_path = 'coordinates.jsonl'
    output_path = 'coordinates_fixed.jsonl'

    clean_data(input_path, output_path)

