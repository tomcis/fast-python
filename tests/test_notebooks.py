import os
from unittest import TestCase

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError

NBS_PATH = "notebooks"
KERNEL_NAME = "python3"


class NotebookTest(TestCase):
    """Unit test notebook"""

    def run_notebook(self, notebook):
        """ Test notebook """

        # load notebook
        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)

        # execute notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name=KERNEL_NAME)
        try:
            ep.preprocess(nb, {})
            status = True
        except CellExecutionError:
            # store if failed
            status = False
            executed_notebook = os.getcwd() + "/" + notebook.split("/")[-1]
            with open(executed_notebook, mode="wt") as f:
                nbformat.write(nb, f)

        # check status
        self.assertTrue(status, "Notebook execution failed (%s)" % notebook)


# @pytest.mark.filterwarnings("ignore:Session._key_changed is deprecated")
class PipelineNotebookTest(NotebookTest):
    """Unit test notebook"""

    def run_tests(self):
        for file in os.listdir(NBS_PATH):
            if file.endswith(".ipynb"):
                self.run_notebook(os.path.join(NBS_PATH, file))
