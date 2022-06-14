import os
import random
import json
from functools import reduce

from .errors import UserError


def is_mixed_type(arr):
    # An enum is said "mixed type" if the enum items don't all have the same type. The only
    # exception to this is NoneType, which is allowed in enums regardless of the type of other
    # items. This allows us to set the value to None when the property is not required.
    if arr:
        return any(not isinstance(e, type(arr[0])) and e != None for e in arr)
    return False


def random_choice(arr):
    # if arr[0][]:
    #     print( "INSIDE 3")
    #     print(len(simulated_data))

    if arr:
        return random.choice(arr)
    return None

def timing_choice(arr, sample):
    # print(arr)
    # print(subjects)

    # print(sample)
    # sample["subjects"] if "subjects" in sample else None,/

    # if sample["type"] == 'lesion_characteristics':
    #     print( "INSIDE 4")
    #     print(len(arr))

    if arr:
        subject_submitter_id = sample["subjects"]["submitter_id"]
        timings_options = [timing for timing in arr if "subjects" in timing and timing["subjects"]["submitter_id"] == subject_submitter_id]
        # if sample["type"] == 'lesion_characteristics' and len(timings_options) == 0:
        #     print( "INSIDE 5")
        #     # print(len(timings_options))
        #     print(sample)
        #     print(arr)
        #     exit()
        # print(timings_options)
        # for timing in arr:
        #     for subject in timing["subjects"]:
        #         if subject["submitter_id"] in subjects_submitter_ids
        return random_choice(timings_options)
    return None


def is_primitive_type(data):
    return isinstance(data, (int, float, str))


def get_keys_list(d):
    def get_field(d, fields):
        return reduce(lambda acc, field: acc.get(field, {}), fields, d)

    result = []
    to_visit = [[key] for key in d.keys()]
    while to_visit:
        key = to_visit.pop()
        result.append(key[-1])
        value = get_field(d, key)
        if isinstance(value, dict):
            to_visit.extend([key + [next_key] for next_key in value.keys()])
    return result


def generate_list_numbers_from_file(data_file, submission_order, n_samples):
    result = []

    try:
        with open(data_file) as f:
            data = json.load(f)
            for filename in submission_order:
                if str(filename) in data:
                    result.append(data[str(filename)])
                else:
                    result.append(n_samples)

    except IOError:
        raise UserError("file {} does not exist".format(data_file))
    except ValueError:
        raise UserError("Can not load json file {}".format(data_file))
    except KeyError as e:
        raise UserError(
            "Missing node in file {}. Detail {}".format(data_file, e.message)
        )

    return result
