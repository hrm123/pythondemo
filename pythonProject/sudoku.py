from utils import grid_values
from utils import display

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a,b):
    return [s+t for s in a for t in b ]

squares = cross(rows, cols)
print('squares')
print('--------------------------')
print( squares)

row_units = [cross(r, cols) for r in rows]
print('row_units')
print('--------------------------')
print( row_units)

col_units = [cross(rows, c) for c in cols]
print('col_units')
print('--------------------------')
print( col_units)

sq_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123','456','789')]
print('sq_units')
print('--------------------------')
print( sq_units)

print('grid_values')
print('--------------------------')
display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..', squares), squares,rows,cols)