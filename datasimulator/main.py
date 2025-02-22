import os
import argparse

from dictionaryutils import DataDictionary, dictionary

from datasimulator.graph import Graph
from datasimulator.submit_data_utils import submit_test_data

from cdislogging import get_logger

logger = get_logger("data-simulator", log_level="info")


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="action", dest="action")

    submission_order_cmd = subparsers.add_parser("submission_order")
    submission_order_cmd.add_argument(
        "--url", required=True, help="s3 dictionary link.", nargs="?"
    )
    submission_order_cmd.add_argument(
        "--node_name", required=False, help="node to generate the submission order for"
    )
    submission_order_cmd.add_argument(
        "--path", required=True, help="path to save file to"
    )

    validation_cmd = subparsers.add_parser("validate")
    validation_cmd.add_argument("--url", required=True, help="s3 dictionary link.")

    simulate_data_cmd = subparsers.add_parser("simulate")
    simulate_data_cmd.add_argument(
        "--url", required=False, help="s3 dictionary link.", nargs="?", default=None
    )
    simulate_data_cmd.add_argument(
        "--path", required=True, help="path to save files to", nargs="?"
    )

    simulate_data_cmd.add_argument(
        "--program", required=False, nargs="?", default="DEV"
    )
    simulate_data_cmd.add_argument(
        "--project", required=False, nargs="?", default="test"
    )

    simulate_data_cmd.add_argument(
        "--max_samples",
        required=False,
        help="max number of samples for each node",
        default=1,
        nargs="?",
    )

    simulate_data_cmd.add_argument(
        "--node_num_instances_file",
        required=False,
        help="max number of samples for each node stored in a file",
        nargs="?",
    )

    simulate_data_cmd.add_argument(
        "--random", help="randomly generate data numbers for nodes", action="store_true"
    )

    simulate_data_cmd.add_argument(
        "--required_only", help="generate only required fields", action="store_true"
    )

    simulate_data_cmd.add_argument(
        "--consent_codes",
        help="include generation of random consent codes",
        action="store_true",
    )

    simulate_data_cmd.add_argument(
        "--skip", help="skip raising an exception if gets an error", action="store_true"
    )

    submit_data_cmd = subparsers.add_parser("submitting_data")
    submit_data_cmd.add_argument("--dir", required=True, help="path containing data")
    submit_data_cmd.add_argument("--host", required=True)
    submit_data_cmd.add_argument("--project", required=True)
    submit_data_cmd.add_argument("--chunk_size", default=1)
    submit_data_cmd.add_argument("--access_token_file", required=True)

    return parser.parse_args()


# python main.py simulate --url https://s3.amazonaws.com/dictionary-artifacts/bhcdictionary/0.4.3/schema.json --path ./data-simulator/sample_test_data --program DEV --project test
def main():
    args = parse_arguments()

    if args.action == "submitting_data":
        logger.info("Submitting data...")
        submit_test_data(
            args.host,
            args.project,
            args.dir,
            args.access_token_file,
            int(args.chunk_size),
        )
        logger.info("Done!")
        return

    logger.info("Data simulator initialization...")
    if args.url:
        logger.info("Loading dictionary from url {}".format(args.url))
        dictionary.init(DataDictionary(url=args.url))
    else:
        logger.info("Loading dictionary from installed dictionary")

    if args.action == "simulate":
        # Initialize graph
        logger.info("Initializing graph...")
        graph = Graph(dictionary, program=args.program, project=args.project)
        graph.generate_nodes_from_dictionary(args.consent_codes)
        graph.construct_graph_edges()
        max_samples = int(args.max_samples)

        # just print error messages
        graph.graph_validation(required_only=args.required_only)

        # simulate data no matter what the graph passes validation or not
        logger.info("Generating data...")
        graph.simulate_graph_data(
            path=args.path,
            n_samples=max_samples,
            node_num_instances_file=args.node_num_instances_file,
            random=args.random,
            required_only=args.required_only,
            skip=args.skip,
        )

    elif args.action == "validate":
        # Initialize graph
        logger.info("Initializing graph...")
        graph = Graph(dictionary)
        graph.generate_nodes_from_dictionary()
        graph.construct_graph_edges()
        logger.info("Validating...")
        graph.graph_validation()

    elif args.action == "submission_order":
        # Initialize graph
        logger.info("Initializing graph...")
        graph = Graph(dictionary)
        graph.generate_nodes_from_dictionary()
        graph.construct_graph_edges()

        logger.info("Generating data submission order...")
        if args.node_name:
            node = graph.get_node_with_name(args.node_name)
            submission_order = graph.generate_submission_order_path_to_node(node)
        else:
            submission_order = graph.generate_submission_order()

        with open(os.path.join(args.path, "DataImportOrderPath.txt"), "w") as outfile:
            for node in submission_order:
                outfile.write(node.name + "\t" + node.category + "\n")

    logger.info("Done!")


if __name__ == "__main__":
    main()
