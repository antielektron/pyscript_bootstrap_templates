
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import HTML as HTML
from pyscript_bootstrap_templates import bootstrap_inputs as bInputs

import numpy as np

# wrapper class to create editable numpy matrices:
class NumpyGrid2D(HTML.Table, bHTML.BootstrapContainer):
    def __init__(self, numpy_grid: np.ndarray, parent: HTML.Element = None):


        # store numpy grid
        self._numpy_grid = numpy_grid.copy()
        m,n = self._numpy_grid.shape

        super().__init__(parent=parent)

        self.m = 0
        self.p = 0

        # create a grid of inputs
        self._inputs = []
        
        for i in range(m):
            row = []
            # to keep it simple: use plain html table elements
            tr = HTML.Tr(parent=self)
            for j in range(n):
                th = HTML.Th(parent=tr)
                cell = bInputs.InputFloat(parent=th)
                cell.p = 0
                cell.m = 0
                cell.value = self._numpy_grid[i,j]
                row.append(cell)
            self._inputs.append(row)
    
    def _update_ndarray(self):
        for i, row in enumerate(self._inputs):
            for j, cell in enumerate(row):
                self._numpy_grid[i,j] = float(cell.value)
                
    
    @property
    def numpy_grid(self) -> np.ndarray:
        self._update_ndarray()
        return self._numpy_grid.copy()
    
    @numpy_grid.setter
    def numpy_grid(self, value:np.ndarray):
        assert value.shape == self._numpy_grid.shape
        self._numpy_grid = value.copy()
        # update input grid

        for i, row in enumerate(self._inputs):
            for j, cell in enumerate(row):
                cell.value = self._numpy_grid[i,j]
    

# create default values
matrix_a = np.array([[1,2,3],[4,5,6],[7,8,9]])
matrix_b = np.array([[1,2,3],[4,5,6],[7,8,9]])

matrix_result = np.zeros((3,3))

app = bootstrap_templates.PyScriptBootstrapDashboard(
    parent_element="pyscript_app", brand_name="03_numpy_grid_demo")
div = bHTML.BootstrapContainer("Matrix operations", parent=app.sidebar)
div.font_size = 4

matrix_row = bHTML.Row(parent=app.main)
matrix_row.p = 1
matrix_row.m = 1
matrix_row.display_property = bHTML.DisplayProperty.INLINE_FLEX

# create row of three matrices
mat_widget_a = NumpyGrid2D(matrix_a)
mat_widget_b = NumpyGrid2D(matrix_b)
mat_widget_result = NumpyGrid2D(matrix_result)

# just for fanciness: wrap the matrices in bootstrap cards
col_a = bHTML.Col(parent=matrix_row)
col_b = bHTML.Col(parent=matrix_row)
col_result = bHTML.Col(parent=matrix_row)

card_a = bHTML.Card(mat_widget_a, card_header=bHTML.Div("Matrix A"), parent=col_a)
card_b = bHTML.Card(mat_widget_b, card_header=bHTML.Div("Matrix B"), parent=col_b)
card_result = bHTML.Card(mat_widget_result, card_header=bHTML.Div("Result"), parent=col_result)

card_a.shadow = bHTML.Shadow.MEDIUM
card_b.shadow = bHTML.Shadow.MEDIUM
card_result.shadow = bHTML.Shadow.MEDIUM

operations = {
    '+': np.add,
    '-': np.subtract,
    '*': np.multiply,
    '/': np.divide,
    'dot product': np.dot
}

for op in operations:
    btn = bHTML.ButtonPrimary(op, parent=app.sidebar)
    btn.w = 100
    btn.m = 1
    def onclick(event, numpy_func=operations[op]):
        mat_widget_result.numpy_grid = numpy_func(mat_widget_a.numpy_grid, mat_widget_b.numpy_grid)
    btn.onclick = onclick




    