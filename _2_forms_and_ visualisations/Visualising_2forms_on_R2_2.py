# Visualising 2-forms on R^2
# Modified such that colour of the lines at each point changes based on the sign of 2-form

# import modules
import timeit
import numpy as np
import matplotlib.pyplot as plt
from sympy import diff
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.lines import Line2D
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D

# %%

# start the timer
start = timeit.default_timer()

'''

define needed fucntions

'''

# define a function to replace input string to be 'python understood'
def format_eq(string):
    # replace all the x and y with xg and yg:
    string = string.replace('x', 'xg')
    string = string.replace('y', 'yg')
    string = string.replace('z', 'zg')
    # where there are special functions, replace them with library directions
    string = string.replace('pi', 'np.pi')
    string = string.replace('sqrt', 'np.sqrt')
    string = string.replace('sin', 'np.sin')
    string = string.replace('cos', 'np.cos')
    string = string.replace('tan', 'np.tan')
    string = string.replace('^', '**')
    string = string.replace('ln', 'np.log')        
    return string


# define a function that takes input string that is python understood and turn into vector components:
def eq_to_comps(string_x, string_y, xg, yg):
    global equation_x, equation_y
    # use this fucntion to replace given string to python understood equations:
    equation_x = format_eq(string_x)
    equation_y = format_eq(string_y)
    # use these to define the field:
    # also: checking if equation equals zero, to then replace it with an array and not just 0:
    u = eval(equation_x)
    v = eval(equation_y)
    if equation_x.find('x') & equation_x.find('y') == -1:
        u = float(equation_x)*np.ones(np.shape(xg))
    if equation_y.find('x') & equation_y.find('y') == -1:
        v = float(equation_y)*np.ones(np.shape(yg))
    # return these
    return u, v


# define a function that will find the 2 form from given expressions
# in a given number of dimensions and in terms of given coordinate symbols
def find_2_form(expressions, coords, m=2):
    global ext_ds, result
    # define a sympy expression for string 0
    sympy_expr_zero = parse_expr('0*x', evaluate=False)
    
    # set up an array to store derrivatives.
    ext_ds = np.empty((m, m), dtype='object')
    
    # set up an array to store the results
    # in 2D only dx^dy, in 3D (in order): dx^dy, dx^dz, dy^dz
    result = np.empty((int((m-1)*m/2), 1), dtype='object')
    for i in range(int((m-1)*m/2)):
        result[i] = str(result[i])
    
    # loop over differentiating each, when differentiating w.r.t its coord, set to 0
    for coord_index in range(len(coords)):
        # loop over differentiating each component:
        for comp_index in range(len(expressions)):
            # when equal set to 0, when not-differentiate:
            if comp_index == coord_index:
                ext_ds[comp_index, coord_index] = str(sympy_expr_zero)
            elif comp_index != coord_index:
                ext_ds[comp_index, coord_index] = str(diff(expressions[comp_index], coords[coord_index]))
            # change the signs for wedges in wrong order
            if comp_index < coord_index:
                ext_ds[comp_index, coord_index] = ' - (' + str(ext_ds[comp_index, coord_index]) + ')'
            elif comp_index > coord_index:
                ext_ds[comp_index, coord_index] = ' + ' + str(ext_ds[comp_index, coord_index])
    
    '''
    merge the results into a 2 form (for 2-form on R^2, the result is a single component (dx^xy))
    do so by adding opposite elements along the diagonal ( / ) components of ext_ds
    this  includes taking elemets with switched i and j
    '''
    
    # set up a variable to count pairs (pairs because we are forming 2 forms):
    pair = 0
    
    # loop over opposing elements (matching elementary 2-forms)
    for i in range(1, m):
        for j in range(i):
            # initially clear the element from its Nonetype placeholder
            result[pair, 0] = ''
            # extract opposing elements
            temp = ext_ds[i, j]
            temp1 = ext_ds[j, i]
            # check these against zero entries:
            if (temp == '0') or (temp == '-(0)') or (temp == '0*x'):
                pass
            else:
                result[pair, 0] += temp
            if (temp1 == '0') or (temp1 == '-(0)') or (temp1 == '0*x'):
                pass
            else:
                result[pair, 0] += temp1
            # update the result row counter
            pair += 1
    # format string in each result row
    for d in range(pair):
        # format the result to be 'python understood' to be able to use the eval()
        result[d, 0] = format_eq(result[d, 0])
    
    # set up a vector to store the 2 form numerically, from xg and yg
    form_2 = np.empty((len(result[:, 0]), pt_den, pt_den))    # Note - need pt_den m times.
    
    # evaluate the expressions again:
    for d in range(0, len(result[:, 0])):
        # numerical evaluation of the 2 form on R^2, at all defined grid points in R^2
        form_2[d, :, :] = eval(result[d, 0])  # Note, need : m times
    
    return form_2


# deifne a fucntion to check number parity
def parity(x):
    '''
    return True when number provided is even and False when it is odd. Checks
    integers only, and not arrays.
    '''
    if x % 2 == 1:
        result = False
    elif x % 2 == 0:
        result = True
    return result


# define function that sets the recursion constant for the loop to plot stacks
# pre-define the displacements from mid point needed
# c is the Truth value from parity (odd or even number n)
def G(s, n, c):
    if c == 0:
        return ((2*s + 1)/(2*(n-1)))
    else:
        return (s/(n-1))


# define a function that will plot stack components, coloured
# as per the orientation of the 2 form at that grid point
def form_2_components_plot(xg, yg, u, v, s_max, L, pt_den, fract, colour_str):
    global s_L
    # get axis lengths:
    x_len = len(xg[:, 0])
    y_len = len(yg[:, 0])
    
    # Scaling of axes and setting equal proportions circles look like circles
    ax.set_aspect('equal')
    ax_L = L + L/delta_factor
    ax.set_xlim(-ax_L, ax_L)
    ax.set_ylim(-ax_L, ax_L)
    
    # define an empty array of magnitudes, to then fill with integer rel. mags
    R_int = np.zeros(shape=((x_len), (y_len)))
    
    # #########################################################################
    # get variables needed for the initial, simplified stack plot
    # #########################################################################
    # find the arrow length corresponding to each point and store in mag array
    mag = np.sqrt(u**2 + v**2)
    # find direction of each arrow
    theta = np.arctan2(v, u)   # theta defined from positive x axis ccw
    
    # #########################################################################
    # use the the direction of arrows to define stack properties
    # #########################################################################
    
    # define length of sheet as a fraction of total graph scale
    sheet_L = L*fract
    # set up the max, total height of stack (along arrow)
    s_L = fract*L
    
    # #########################################################################
    # define the stacks based on geometrical arguments
    # to be perp. to arrow. shifted parallel to it, their density porp to mag
    # of the arrow and with an arrowhead on top.
    # #########################################################################
    # find the maximum magnitude for scaling
    max_size = np.max(mag)   # careful with singularities, else ---> nan
    
    # find the relative magnitude of vectors to maximum, as an array
    R = mag/max_size
    
    # define tigonometirc shifts
    I_sin = np.sin(theta)
    I_cos = np.cos(theta)
    
    # define the points that set out a line of the stack sheet (middle line)
    A_x = xg + (sheet_L/2)*np.sin(theta)
    A_y = yg - (sheet_L/2)*np.cos(theta)
    B_x = xg - (sheet_L/2)*np.sin(theta)
    B_y = yg + (sheet_L/2)*np.cos(theta)
    
    # loop over each arrow coordinate in x and y
    for i in range(x_len):
        for j in range(y_len):
            # define it for all magnitudes. Separately for odd and even corr. number of sheets:
            # Label each element with the number of stacks required: linear scaling
            
            if form_2_sgn[i, j] == +1:
                color_index = 0
            elif form_2_sgn[i, j] == -1:
                color_index = 1
            else:
                color_index = 2  # just in case
            
            for t in range(1, s_max+1):
                if (t-1)/s_max <= R[i, j] <= t/s_max:
                    R_int[i, j] = t
            # set a varible for current considered magnitude as it is reused
            # avoids extracting from R many times.
            n = R_int[i, j]
            
            # deal with even number of sheets from magnitudes:
            if parity(n) is True:
                # define a parameter to loop over in the recursion equation
                s = 0
                
                # Define the points for sheets required for the given magnitude
                # from these define all the needed lines and plot them
                while s <= 0.5*(n-2):  # maximum set by equations (documentation)
                    # define all the points for the 2 currently looped +- sheets in while loop
                    Ax1 = A_x[i, j] + G(s, n, 0)*s_L*I_cos[i, j]
                    Ay1 = A_y[i, j] + G(s, n, 0)*s_L*I_sin[i, j]
                    Bx1 = B_x[i, j] + G(s, n, 0)*s_L*I_cos[i, j]
                    By1 = B_y[i, j] + G(s, n, 0)*s_L*I_sin[i, j]
                    Ax2 = A_x[i, j] - G(s, n, 0)*s_L*I_cos[i, j]
                    Ay2 = A_y[i, j] - G(s, n, 0)*s_L*I_sin[i, j]
                    Bx2 = B_x[i, j] - G(s, n, 0)*s_L*I_cos[i, j]
                    By2 = B_y[i, j] - G(s, n, 0)*s_L*I_sin[i, j]
                    
                    # from these, define the 2 lines, for this run
                    ax.add_line(Line2D((Ax1, Bx1), (Ay1, By1), linewidth=0.5, color=colour_str[color_index]))
                    ax.add_line(Line2D((Ax2, Bx2), (Ay2, By2), linewidth=0.7, color=colour_str[color_index]))
                    
                    # update parameter to reapet and draw all needed arrows
                    s += 1
            # deal with the odd number of stacks:
            elif parity(n) is False:
                # Add the centre line for odd numbers of stacks
                ax.add_line(Line2D((A_x[i, j], B_x[i, j]), (A_y[i, j], B_y[i, j]), linewidth=0.7, color=colour_str[color_index]))
                
                # then loop over the remaining lines as per the recursion formula:
                s = 1  # change the looping parametr to exclude already completed 0 (corr. to middle sheet here)
                
                # define all remaining sheets for the magnitude:
                while s <= 0.5*(n-1):  # maximum set by equations (documentation)
                    # define all the points for the current +- displacement in while loop
                    Ax1 = A_x[i, j] + G(s, n, 1)*s_L*I_cos[i, j]
                    Ay1 = A_y[i, j] + G(s, n, 1)*s_L*I_sin[i, j]
                    Bx1 = B_x[i, j] + G(s, n, 1)*s_L*I_cos[i, j]
                    By1 = B_y[i, j] + G(s, n, 1)*s_L*I_sin[i, j]
                    Ax2 = A_x[i, j] - G(s, n, 1)*s_L*I_cos[i, j]
                    Ay2 = A_y[i, j] - G(s, n, 1)*s_L*I_sin[i, j]
                    Bx2 = B_x[i, j] - G(s, n, 1)*s_L*I_cos[i, j]
                    By2 = B_y[i, j] - G(s, n, 1)*s_L*I_sin[i, j]
                    
                    # from these, define the 2 displaced lines
                 
                    ax.add_line(Line2D((Ax1,Bx1),(Ay1,By1), linewidth=0.7, color=colour_str[color_index]))
                    ax.add_line(Line2D((Ax2,Bx2),(Ay2,By2), linewidth=0.7, color=colour_str[color_index]))
                    
                    # change the parameter to loop over all changes in displacement for current magnitude
                    s += 1

'''

Set up all needed parameters, plots etc and complete the 2 form figure for the given filed

'''

# define scale of the graph
L = 5
pt_den = 20   # number of points on each axis

# define x and y values
x = np.linspace(-L, L, pt_den)
y = np.linspace(-L, L, pt_den)

# create the grids
xg, yg = np.meshgrid(x, y)

# define an example vector field, now - from string, even initially
string_x = 'x*sin(y)'  # x component
string_y = 'y*cos(x)'  # y component

# to define a 2 from, need to perform the exterior derrivative on
# the given 1 form (vector field).
# To do this, seed to define partial derrivatives.
# to make it general, need to define it through derrivatives w.r.t. not
# already present coordinates.

# set the dimensionality
m = 2

# take the input strings and turn them into sympy expressions to be able to
# use sympy's partial differentiation
sympy_expr_x = parse_expr(string_x, evaluate=False)
sympy_expr_y = parse_expr(string_y, evaluate=False)
# for m > 2, need more components, and need these in 'expressions' too!

# combine the 2 into a list:
expressions = np.array([sympy_expr_x, sympy_expr_y])

# use sympy partial derrivatives on these, as to get a 2-form on R2:
# need to differentiate each component w.r.t the coordinates that it's
# elementary 1 form does not contain.

# set up an array of coordinates that need to be used (in standard order)
coords = ['x', 'y']

# from these, use the find_2_form function to get the 2 form
form_2 = find_2_form(expressions, coords, m)

# get the signs of the 2 form
form_2_sgn = np.sign(form_2[0])

# evaluate the u and v given previously, with formating for them to be
# python understood
u, v = eq_to_comps(str(expressions[0]), str(expressions[1]), xg, yg)

# set up a zero vector filed to plot x and y components as 2 separate fields:
zero_field = np.zeros(np.shape(xg))

# set up the delta_factor of additional axis space L/delta_factor gives extra space on axis
delta_factor = 10

# fraction of sheet length to graph length
fract = 0.05

# define the maximum number of stack to plot, dep. on magnitude
s_max = 5
    
# create a figure
fig = plt.figure(figsize=(8, 8))

# set up axis
ax = fig.gca()

# set up visuals - axis labels
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

# Scaling of axes and setting equal proportions circles look like circles
ax.set_aspect('equal')
ax_L = L + L/delta_factor
ax.set_xlim(-ax_L, ax_L)
ax.set_ylim(-ax_L, ax_L)

# set up a colour string for the orientations
# first string defines colour for positive (ccw), second for negative (cw)
# last one is an in case, for when the magnitude is exactly zero.
colour_str = ['red', 'blue', 'grey']

# plot the fields with desired parameters as specidfied above
# arrow params not needed as arrows arent plotted
form_2_components_plot(xg, yg, u, zero_field, s_max, L, pt_den, fract, colour_str)
form_2_components_plot(xg, yg, zero_field, v, s_max, L, pt_den, fract, colour_str)
# these fields are the original components

# Create new figure for 2-form contour/surface plots
fig1 = plt.figure()
fig1.suptitle('2-form Surface')
ax1 = fig1.gca(projection='3d')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

# Using the 2-form expression, plot z = F(x,y) as a contour/surface, comment as required
zg = eval(format_eq(ext_ds[1,0]+ext_ds[0,1]))
# C_plot = ax1.contour(xg,yg,zg,50)
S_plot = ax1.plot_surface(xg,yg,zg,cmap=cm.coolwarm)

# return time to run
stop = timeit.default_timer()
print('Time to run: ', stop - start)