from utils import grid_values
from utils import display, parse_grid
from utils import test_sudoku_setup 

# https://norvig.com/sudoku.html
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a,b):
    return [s+t for s in a for t in b ]

cells = cross(rows, cols)
print('cells')
print('--------------------------')
print( cells)

row_cells = [cross(r, cols) for r in rows]
print('row_cells')
print('--------------------------')
print( row_cells)

col_cells = [cross(rows, c) for c in cols]
print('col_cells')
print('--------------------------')
print( col_cells)

sq_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123','456','789')]
print('sq_units')
print('--------------------------')
print( sq_units)

print('grid_values')
print('--------------------------')
display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..', cells), cells,rows,cols)

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

print('col_cells')
print('--------------------------')
print( col_cells)

units = dict((s, [u for u in unitlist if s in u]) 
             for s in cells)
print('unitlist')
print('--------------------------')
print( unitlist)

print('units')
print('--------------------------')
print(units)

peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in cells)
print('peers')
print('--------------------------')
print( peers)

test_sudoku_setup(cells, unitlist, units, peers)


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

display(parse_grid(grid1,cells,units, peers),cells,rows,cols)
