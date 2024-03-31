from utils import test_sudoku_setup, display
import resource, sys
print(sys.getrecursionlimit())
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(100)
print(sys.getrecursionlimit())

logFile = open('log.txt', 'w')

# https://norvig.com/sudoku.html
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a,b):
    return [s+t for s in a for t in b ]

boxes = cross(rows, cols)

print('boxes')
print('--------------------------')
print( boxes)

row_units = [cross(r, cols) for r in rows]
print('row_units')
print('--------------------------')
print( row_units)

column_units = [cross(rows, c) for c in cols]
print('column_units')
print('--------------------------')
print( column_units)

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
print('square_units')
print('--------------------------')
print( square_units)

unitlist = row_units + column_units + square_units
print('unitlist')
print('--------------------------')
print( unitlist)

def grid_values_(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    result = dict(zip(boxes, values))
    return result


units = dict((s, [u for u in unitlist if s in u]) 
             for s in boxes)


print('units')
print('--------------------------')
print(units)


print('units-c2')
print('--------------------------')
print(units['C2'])

peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in boxes)
print('peers')
print('--------------------------')
print( peers)

test_sudoku_setup(boxes, unitlist, units, peers)


def grid_values_(sudokuBoardStr):
    """Convert sudokuBoardStr string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in sudokuBoardStr:
        if c == '0' or c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    result = dict(zip(boxes, values))
    return result

grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

def eliminate_(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

# different way to combine elimination & only choice strategies - iterative
def reduce_puzzle(values):
    # digits   = '123456789'
    ## To start, every square can be any digit; then assign values from the grid.
    # values = dict((s, digits) for s in boxes)
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate_(values) # constraint propogation - when we apply constraint sof each square it generates further cosntraints on related squares reducing search space
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    print('old values = ', file=logFile)
    print(values, file=logFile)
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    print('new values = ', file=logFile)
    print(values, file=logFile)
    print('-----------------------------', file=logFile)

    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


# result - solves
#grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#resultFinal = search(grid_values_(grid2))
#print('stalled='+ ('True' if resultFinal is False else 'False'))
#display(resultFinal,boxes,rows,cols)

# result - solves
#grid2 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
#resultFinal2 = reduce_puzzle(grid_values_(grid2))
#print('stalled='+ ('True' if resultFinal2 is False else 'False'))
#display(resultFinal2,boxes,rows,cols)

# result - stalled
#grid3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#resultFinal3 = reduce_puzzle(grid_values_(grid3))
#print('stalled='+ ('True' if resultFinal3 is False else 'False'))
#display(resultFinal3,boxes,rows,cols)
        
# with search
# result - solves
#grid3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#resultFinal3 = search(grid_values_(grid3))
#print('stalled='+ ('True' if resultFinal3 is False else 'False'))
#display(resultFinal3,boxes,rows,cols)


# result - solves
#grid2 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
#resultFinal2 = reduce_puzzle(grid_values_(grid2))
#print('stalled='+ ('True' if resultFinal2 is False else 'False'))
#display(resultFinal2,boxes,rows,cols)

# result - stalled
#grid3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#resultFinal3 = reduce_puzzle(grid_values_(grid3))
#print('stalled='+ ('True' if resultFinal3 is False else 'False'))
#display(resultFinal3,boxes,rows,cols)

# result - solves
grid3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
resultFinal3 = search(grid_values_(grid3))
print('stalled='+ ('True' if resultFinal3 is False else 'False'))
display(resultFinal3,boxes,rows,cols)