import sys
import os
from chaste_database_connector import *


def main():
    assert len(sys.argv) in (2,3), f'Usage: {sys.argv[0]} [EXPERIMENT_NAME] [OPTIONAL|DATABASE_FILE]'
    assert os.path.exists(sys.argv[1])
    experiment_folder = os.path.abspath(sys.argv[1])
    create_database(recreate=False)
    load_defaults()
    retrieve(experiment_folder)
    

if __name__ == "__main__":
    main()