import os
os.environ['ETS_TOOLKIT'] = 'qt4'

 
from mayavi import mlab
from tvtk.api import tvtk
from tvtk.common import configure_input_data
from tvtk.pyface.api import Scene
from numpy import arange, nonzero, float32, min, max, median, copy, random, shape
from numpy.core.numeric import ravel
 
from traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict
from traitsui.api import View, Item, VGroup, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor


from pyface.qt import QtGui, QtCore

import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import df3_for_gui as df3





lft = -5
rght = 5
pts = 10



class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    view = View(Item('scene', 
                     editor=SceneEditor(scene_class=MayaviScene),
                     height=250, 
                     width=300, 
                     show_label=False),
                resizable=True
                )
 
    needUpdate = None


    def clear(self):
        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()


 
    def takePlotParametresF1(self, stck_coords, red_balls_data_f1, axes_limits_f1):

        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()
        self.stck_coords = stck_coords
        self.red_balls_data_f1 = red_balls_data_f1
        self.axes_limits_f1 = axes_limits_f1

        self.needUpdate = True
 
        self.update_plot_f1()

    def takePlotParametresVF(self, fld_comps, red_balls_data_vf, axes_limits_vf, cmap_vs_clr_idx, clrmap, vecclr, sngclr):

        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()
        self.fld_comps = fld_comps
        self.red_balls_data_vf = red_balls_data_vf
        self.axes_limits_vf = axes_limits_vf
        self.cmap_vs_clr_idx = cmap_vs_clr_idx
        self.clrmap = clrmap
        self.vecclr = vecclr
        self.sngclr = sngclr

        self.needUpdate = True
 
        self.update_plot_vf()

    def takePlotParametresF0(self, sc_fld, axes_limits_f0):

        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()
        self.sc_fld = sc_fld
        self.axes_limits_f0 = axes_limits_f0
        
        self.needUpdate = True
 
        self.update_plot_f0()

    def takePlotParametresF2(self, xg, yg, zg, fx, fy, fz, fx_eqn, fy_eqn, fz_eqn):

        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()
        self.x = xg
        self.y = yg
        self.z = zg
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.fx_eqn = fx_eqn
        self.fy_eqn = fy_eqn
        self.fz_eqn = fz_eqn
        
        self.needUpdate = True
 
        self.update_plot_f2()

    def takePlotParametresF3(self, xg3, yg3, zg3, f3, f3_eqn):

        self.scene.mlab.clf()
        self.scene.renderer.remove_all_view_props()
        self.x3 = xg3
        self.y3 = yg3
        self.z3 = zg3
        self.f3 = f3
        self.f3_eqn = f3_eqn


        
        self.needUpdate = True
 
        self.update_plot_f3()

        
 
    @on_trait_change('scene.activated')
    def update_plot_f1(self):

        if not self.needUpdate:
            vtext = tvtk.VectorText()
            vtext.text = 'DFormPy 3D'
            text_mapper = tvtk.PolyDataMapper()
            configure_input_data(text_mapper, vtext.get_output())
            vtext.update()
            p2 = tvtk.Property(color=(0, 0.3, 0.3))
            text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
            text_actor.position = (0, 0, 0)
            self.scene.add_actor(text_actor)

        else:

            self.scene.add_actor(self.stck_coords[0])
            self.scene.add_actor(self.stck_coords[1])
            self.scene.add_actor(self.stck_coords[2])
            self.scene.add_actor(self.stck_coords[3])
            self.scene.add_actor(self.stck_coords[4])
            self.scene.add_actor(self.stck_coords[5])

            self.scene.mlab.points3d(self.red_balls_data_f1[0],
                                    self.red_balls_data_f1[1],
                                    self.red_balls_data_f1[2], color = (1,0,0),scale_factor=self.red_balls_data_f1[3], resolution=36)


            self.ax = self.scene.mlab.axes(color = (0,0,0), nb_labels = 5, extent = self.axes_limits_f1, line_width=1.0)
            self.ax.axes.font_factor = 0.5


        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)


    def update_plot_vf(self):

        if not self.needUpdate:
            vtext = tvtk.VectorText()
            vtext.text = 'DFormPy 3D'
            text_mapper = tvtk.PolyDataMapper()
            configure_input_data(text_mapper, vtext.get_output())
            vtext.update()
            p2 = tvtk.Property(color=(0, 0.3, 0.3))
            text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
            text_actor.position = (0, 0, 0)
            self.scene.add_actor(text_actor)

        else:

            self.scene.mlab.points3d(self.red_balls_data_vf[0],
                                    self.red_balls_data_vf[1],
                                    self.red_balls_data_vf[2], color = (self.sngclr[0]/255, self.sngclr[1]/255, self.sngclr[2]/255),scale_factor=self.red_balls_data_vf[3], resolution=36)
            
            if self.cmap_vs_clr_idx==0:
                qivfld = self.scene.mlab.quiver3d(self.fld_comps[0], self.fld_comps[2], self.fld_comps[4], self.fld_comps[1], self.fld_comps[3], self.fld_comps[5],\
                                colormap=self.clrmap, color=None, line_width=1.0, mode='arrow',\
                                scale_factor=0.1, scale_mode = 'vector', opacity = 1)
                cbar = self.scene.mlab.vectorbar(object=qivfld)
                cbar.scalar_bar.unconstrained_font_size = True
                cbar.label_text_property.font_size=10
                cbar.scalar_bar_representation.orientation=1
                cbar.scalar_bar_representation.position = [0.05, 0.05]
                cbar.scalar_bar_representation.position2 = [0.05, 0.85]

                
                
            if self.cmap_vs_clr_idx==1:
                self.scene.mlab.quiver3d(self.fld_comps[0], self.fld_comps[2], self.fld_comps[4], self.fld_comps[1], self.fld_comps[3], self.fld_comps[5],\
                                color=(self.vecclr[0]/255, self.vecclr[1]/255, self.vecclr[2]/255), line_width=1.0, mode='arrow',\
                                scale_factor=0.1, scale_mode = 'vector', opacity = 1)

            self.ax = self.scene.mlab.axes(color = (0,0,0), nb_labels = 5, line_width=1.0)
            self.ax.axes.font_factor = 0.5

        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)
 
    
    def update_plot_f0(self):

        if not self.needUpdate:
            vtext = tvtk.VectorText()
            vtext.text = 'DFormPy 3D'
            text_mapper = tvtk.PolyDataMapper()
            configure_input_data(text_mapper, vtext.get_output())
            vtext.update()
            p2 = tvtk.Property(color=(0, 0.3, 0.3))
            text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
            text_actor.position = (0, 0, 0)
            self.scene.add_actor(text_actor)

        else:

            cnt = self.scene.mlab.contour3d(self.sc_fld, colormap='jet', opacity = 0.5, contours=7)
            
            self.scene.mlab.colorbar(object = cnt, orientation='vertical')

            self.scene.mlab.outline(line_width=1.0)
            self.ax = self.scene.mlab.axes(color = (0,0,0), ranges=(lft,rght,lft,rght,lft,rght), nb_labels = 5, line_width=1.0)
            self.ax.axes.font_factor = 0.5

        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)
 

    def update_plot_f2(self):

        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)

        if not self.needUpdate:
            vtext = tvtk.VectorText()
            vtext.text = 'DFormPy 3D'
            text_mapper = tvtk.PolyDataMapper()
            configure_input_data(text_mapper, vtext.get_output())
            vtext.update()
            p2 = tvtk.Property(color=(0, 0.3, 0.3))
            text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
            text_actor.position = (0, 0, 0)
            self.scene.add_actor(text_actor)

        else:

            f2 = df3.form_2_3d(self.x, self.y, self.z, self.fx, self.fy, self.fz)
            f2.give_eqn(self.fx_eqn, self.fy_eqn, self.fz_eqn)
            f2.plot(self.scene)

 
    def update_plot_f3(self):

        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)

        if not self.needUpdate:
            vtext = tvtk.VectorText()
            vtext.text = 'DFormPy 3D'
            text_mapper = tvtk.PolyDataMapper()
            configure_input_data(text_mapper, vtext.get_output())
            vtext.update()
            p2 = tvtk.Property(color=(0, 0.3, 0.3))
            text_actor = tvtk.Follower(mapper=text_mapper, property=p2)
            text_actor.position = (0, 0, 0)
            self.scene.add_actor(text_actor)

        else:

            f3 = df3.form_3_3d(self.x3, self.y3, self.z3, self.f3)
            f3.give_eqn(self.f3_eqn)
            f3.plot(self.scene)



 







 
################################################################################

 
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        layout = QtGui.QGridLayout(self)

        layout.setSpacing(0)
        self.visualization = Visualization()

        spc = QtGui.QLabel('')


        self.label1 = QtGui.QLabel('dx')
        self.label1.setAlignment(Qt.AlignCenter)
        self.line_edit1 = QtGui.QLineEdit("1/y")
        self.box1 = QRadioButton(" ")
        self.box1.setEnabled(False)

        self.label2 = QtGui.QLabel('dy')
        self.label2.setAlignment(Qt.AlignCenter)
        self.line_edit2 = QtGui.QLineEdit("-1/x")
        self.box2 = QRadioButton(" ")
        self.box2.setEnabled(False)

        self.label3 = QtGui.QLabel('dz')
        self.label3.setAlignment(Qt.AlignCenter)
        self.line_edit3 = QtGui.QLineEdit("0")
        self.box3 = QRadioButton(" ")
        self.box3.setEnabled(False)

        self.combobox1 = QtGui.QComboBox()
        self.combobox1.addItems(['Covariant Field (Vector Field)', '0-form (Scalar Field)', '1-form', '2-form', '3-form'])
        self.combobox1.setCurrentIndex(0)
        self.combobox1.currentIndexChanged.connect(self.dropbox_option_UI_change)

        self.sublayout1 = QtGui.QHBoxLayout()
        self.sublayout1.addWidget(self.line_edit1)
        self.sublayout1.addWidget(self.box1, alignment=Qt.AlignRight)
        self.sublayout1.setSpacing(5)

        self.sublayout2 = QtGui.QHBoxLayout()
        self.sublayout2.addWidget(self.line_edit2)
        self.sublayout2.addWidget(self.box2, alignment=Qt.AlignRight)
        self.sublayout2.setSpacing(5)

        self.sublayout3 = QtGui.QHBoxLayout()
        self.sublayout3.addWidget(self.line_edit3)
        self.sublayout3.addWidget(self.box3, alignment=Qt.AlignRight)
        self.sublayout3.setSpacing(5)
        
        

#==========================================================================================================
#================================= UI elemnts =============================================================
#==========================================================================================================

#------------------------------------- Axes ---------------------------------------------------------------



        self.groupbox_ax_param = QGroupBox("Axes parameters")
        self.grpbox_host_layout = QVBoxLayout()
        
        self.foc_pt_layout = QtGui.QHBoxLayout()
        self.foc_pt_x_lbl = QtGui.QLabel('x:')
        self.foc_pt_x = QtGui.QLineEdit("0")
        self.foc_pt_x.setMaximumWidth(50)
        self.foc_pt_y_lbl = QtGui.QLabel('y:')
        self.foc_pt_y = QtGui.QLineEdit("0")
        self.foc_pt_y.setMaximumWidth(50)
        self.foc_pt_z_lbl = QtGui.QLabel('z:')
        self.foc_pt_z = QtGui.QLineEdit("0")
        self.foc_pt_z.setMaximumWidth(50)
        self.foc_pt_layout.addWidget(self.foc_pt_x_lbl)
        self.foc_pt_layout.addWidget(self.foc_pt_x, alignment=Qt.AlignLeft)
        self.foc_pt_layout.addWidget(self.foc_pt_y_lbl)
        self.foc_pt_layout.addWidget(self.foc_pt_y, alignment=Qt.AlignLeft)
        self.foc_pt_layout.addWidget(self.foc_pt_z_lbl)
        self.foc_pt_layout.addWidget(self.foc_pt_z, alignment=Qt.AlignLeft)


        self.range_layout = QtGui.QHBoxLayout()
        self.range = QtGui.QLineEdit("10")
        self.range_label = QtGui.QLabel('Axes size')
        self.range_layout.addWidget(self.range, alignment=Qt.AlignRight)
        self.range_layout.addWidget(self.range_label, alignment=Qt.AlignLeft)

        self.pts_layout = QtGui.QHBoxLayout()
        self.pts = QtGui.QLineEdit("10")
        self.pts_label = QtGui.QLabel('Number of points')
        self.pts_layout.addWidget(self.pts, alignment=Qt.AlignRight)
        self.pts_layout.addWidget(self.pts_label, alignment=Qt.AlignLeft)

        self.grpbox_host_layout.addWidget(QtGui.QLabel('Point of focus'), alignment=Qt.AlignCenter)
        self.grpbox_host_layout.addLayout(self.foc_pt_layout)
        self.grpbox_host_layout.addLayout(self.range_layout)
        self.grpbox_host_layout.addLayout(self.pts_layout)

        self.groupbox_ax_param.setLayout(self.grpbox_host_layout)


#----------------------------------------------------------------------------------------------------------

#-------------------------------- Scaling dials -----------------------------------------------------------

        self.groupbox_scaling = QGroupBox("Scaling")
        self.dial_host_layout = QtGui.QHBoxLayout()
        

        self.dial_stack = QDial()
        self.dial_stack.setMaximum(10000)
        self.dial_stack.setMinimum(0)
        self.dial_stack.setValue(1000)
        self.dial_redball = QDial()
        self.dial_redball.setMaximum(10000)
        self.dial_redball.setMinimum(0)
        self.dial_redball.setValue(1000)

        self.dial_stack_label = QLabel("Stacks")
        self.dial_redball_label = QLabel("Singularities")

        self.stack_dial_val = QLabel("1.0")
        self.redball_dial_val = QLabel("1.0")

        self.dial_stack_layout = QVBoxLayout()
        self.dial_stack_layout.setSpacing(1)
        self.dial_redball_layout = QVBoxLayout()
        self.dial_redball_layout.setSpacing(1)

        def dial_method():
            value_stck = self.dial_stack.value()
            self.stack_dial_val.setText("x{}".format(str(value_stck/1000)))

            value_rdbll = self.dial_redball.value()
            self.redball_dial_val.setText("x{}".format(str(value_rdbll/1000)))

        self.dial_stack.valueChanged.connect(lambda: dial_method())
        #self.dial_stack.valueChanged.connect(lambda: self.create_df3_plot())
        self.dial_redball.valueChanged.connect(lambda: dial_method())
        #self.dial_redball.valueChanged.connect(lambda: self.create_df3_plot())

        self.dial_stack_layout.addWidget(self.stack_dial_val, alignment=Qt.AlignCenter)
        self.dial_stack_layout.addWidget(self.dial_stack)
        self.dial_stack_layout.addWidget(self.dial_stack_label, alignment=Qt.AlignCenter)
        self.dial_redball_layout.addWidget(self.redball_dial_val, alignment=Qt.AlignCenter)
        self.dial_redball_layout.addWidget(self.dial_redball)
        self.dial_redball_layout.addWidget(self.dial_redball_label, alignment=Qt.AlignCenter)

        self.dial_host_layout.addLayout(self.dial_stack_layout)
        self.dial_host_layout.addLayout(self.dial_redball_layout)

        self.groupbox_scaling.setLayout(self.dial_host_layout)

#-----------------------------------------------------------------------------------------------------------------

#-------------------------------- Cosmetics ----------------------------------------------------------------------



        self.groupbox_cosmetic = QGroupBox("Cosmetics")
        self.cosmetics_host_layout = QtGui.QVBoxLayout()

        self.rgb_vec = [255, 0, 0]
        self.rgb_sng = [255, 0, 0]
        self.clr_vs_cmap_idx = [0, 1] # 0 for cmap, 1 for clr

        def idx(val):
            print(self.clr_vs_cmap_idx[val])

        def VecClrToggled():
            col = QColorDialog.getColor()
            hex = col.name().lstrip('#')
            rgb = [int(hex[i:i+2], 16) for i in (0, 2, 4)]
            self.frame.setStyleSheet("background-color: rgba({}, {}, {}, 255)".format(rgb[0],rgb[1],rgb[2]))
            self.rgb_vec = rgb

        def SingClr():
            col = QColorDialog.getColor()
            hex = col.name().lstrip('#')
            rgb = [int(hex[i:i+2], 16) for i in (0, 2, 4)]
            self.frame_sing.setStyleSheet("background-color: rgba({}, {}, {}, 255)".format(rgb[0],rgb[1],rgb[2]))
            self.rgb_sng = rgb

        self.vector_colourmap_layout = QtGui.QHBoxLayout()
        self.vec_cmap_lbl = QLabel("V. colourmap")
        self.vec_cmap_chckbox = QRadioButton()
        self.vec_cmap_chckbox.setChecked(True)
        self.vector_colourmap_layout.addWidget(self.vec_cmap_chckbox, alignment=Qt.AlignLeft)
        self.vector_colourmap_layout.addWidget(self.vec_cmap_lbl, alignment=Qt.AlignLeft)
        self.cmap_list = QComboBox()
        self.cmap_list.addItems(["afmhot","autumn","binary","bone","cool","copper","gist_earth","gist_heat",
                                 "gist_rainbow","gnuplot","gnuplot2","hot","inferno","jet","ocean","pink",
                                 "plasma","spring","summer","turbo","viridis","winter","Wistia"])
        self.vector_colourmap_layout.addWidget(self.cmap_list, alignment=Qt.AlignLeft)
        self.vector_colourmap_layout.setSpacing(5)
        self.vector_colourmap_layout.setAlignment(Qt.AlignLeft)

        self.vector_colour_layout = QtGui.QHBoxLayout()
        self.vec_clr_lbl = QLabel("Vector colour")
        self.vec_clr_lbl.setDisabled(True)
        self.vec_clr_chckbox = QRadioButton()
        self.vector_colour_layout.addWidget(self.vec_clr_chckbox, alignment=Qt.AlignLeft)
        self.vector_colour_layout.addWidget(self.vec_clr_lbl, alignment=Qt.AlignLeft)
        self.frame = QPushButton(" ")
        self.frame.clicked.connect(lambda: VecClrToggled())
        self.frame.setStyleSheet("background-color: rgba(255, 0, 0, 50)")
        self.vector_colour_layout.addWidget(self.frame, alignment=Qt.AlignLeft)
        self.vector_colour_layout.setSpacing(5)
        self.vector_colour_layout.setAlignment(Qt.AlignLeft)

        self.cmap_layout = QtGui.QHBoxLayout()
        self.cmap = QPushButton("")
        self.cmap.setStyleSheet("background-image: url(./cmaps/{}.png)".format(self.cmap_list.currentText()))
        self.cmap_list.currentTextChanged.connect(lambda: self.cmap.setStyleSheet("background-image: url(./cmaps/{}.png)".format(self.cmap_list.currentText())))
        self.cmap.setMinimumWidth(150)
        self.cmap.setDisabled(True)
        self.cmap_layout.addWidget(self.cmap, alignment=Qt.AlignRight)

        self.sing_colour_layout = QtGui.QHBoxLayout()
        self.sing_colour_layout.addWidget(QLabel("Singularity colour"), alignment=Qt.AlignLeft)
        self.frame_sing = QPushButton(" ")
        self.frame_sing.clicked.connect(lambda: SingClr())
        self.frame_sing.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.sing_colour_layout.addWidget(self.frame_sing, alignment=Qt.AlignLeft)
        self.sing_colour_layout.setSpacing(5)
        self.sing_colour_layout.setAlignment(Qt.AlignLeft)



        self.vec_clr_chckbox.toggled.connect(lambda: self.vec_cmap_chckbox.setChecked(False))
        self.vec_clr_chckbox.toggled.connect(self.cmap_list.setDisabled)
        self.vec_clr_chckbox.toggled.connect(self.vec_cmap_lbl.setDisabled)
        self.vec_clr_chckbox.toggled.connect(lambda: self.frame.setStyleSheet("background-color : rgba({}, {}, {}, 255)".format(self.rgb_vec[0],self.rgb_vec[1],self.rgb_vec[2])))
        self.vec_clr_chckbox.toggled.connect(lambda: self.vec_clr_lbl.setDisabled(False))
        self.vec_clr_chckbox.toggled.connect(lambda: idx(1))
        #self.vec_clr_chckbox.toggled.connect(lambda: print(self.clr_vs_cmap_idx))

        self.vec_cmap_chckbox.toggled.connect(lambda: self.vec_clr_chckbox.setChecked(False))
        self.vec_cmap_chckbox.toggled.connect(self.frame.setDisabled)
        self.vec_cmap_chckbox.toggled.connect(lambda: self.frame.setStyleSheet("background-color : rgba({}, {}, {}, 50)".format(self.rgb_vec[0],self.rgb_vec[1],self.rgb_vec[2])))
        self.vec_cmap_chckbox.toggled.connect(lambda: self.vec_clr_lbl.setDisabled(True))
        self.vec_cmap_chckbox.toggled.connect(lambda: idx(0))
        #self.vec_cmap_chckbox.toggled.connect(lambda: print(self.clr_vs_cmap_idx))


        self.cosmetics_host_layout.addLayout(self.vector_colourmap_layout)
        self.cosmetics_host_layout.addLayout(self.cmap_layout)
        self.cosmetics_host_layout.addLayout(self.vector_colour_layout)
        self.cosmetics_host_layout.addLayout(self.sing_colour_layout)

        self.groupbox_cosmetic.setLayout(self.cosmetics_host_layout)

    
#-----------------------------------------------------------------------------------------------------------------

#---------------------------------------- DFormPy 3D methods -----------------------------------------------------

        self.groupbox = QGroupBox()

        self.df3_host_layout = QVBoxLayout()

        # -=-=-=-=-=-=- Div -=-=-=-=-=-=-

        self.divrgence_lout = QHBoxLayout()
        self.div_lbl = QLabel("Divergence at ({}, {}, {}): ".format(self.foc_pt_x.text(), self.foc_pt_y.text(), self.foc_pt_z.text()))
        self.div_val = QLineEdit()
        self.div_val.setReadOnly(True)

        self.divrgence_lout.addWidget(self.div_lbl, alignment=Qt.AlignLeft)
        self.divrgence_lout.addWidget(self.div_val, alignment=Qt.AlignLeft)
        self.divrgence_lout.addWidget(QLabel(" "))
        self.divrgence_lout.addWidget(QLabel(" "))
        self.divrgence_lout.setSpacing(10)

        # -=-=-=-=-=-=- Curl -=-=-=-=-=-=-

        self.curl_lout = QHBoxLayout()
        self.curl_btn_lout = QVBoxLayout()
        self.curl_btn_lout.setSpacing(5)
        self.preserve_fld_lout = QHBoxLayout()
        self.fld_inc_chckbx = QCheckBox()
        self.preserve_fld_lout.addWidget(QLabel("include field"), alignment=Qt.AlignRight)
        self.preserve_fld_lout.addWidget(self.fld_inc_chckbx)
        self.curl_button = QPushButton("Curl")
        self.curl_btn_lout.addWidget(self.curl_button)
        self.curl_btn_lout.addLayout(self.preserve_fld_lout)

        self.curl_lout.addLayout(self.curl_btn_lout)
        self.curl_lout.addWidget(QLabel(" "))
        self.curl_lout.addWidget(QLabel("Cosmetics"), alignment=Qt.AlignCenter)
        self.curl_lout.addWidget(QLabel(" "))


        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        self.df3_host_layout.addLayout(self.divrgence_lout)
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addLayout(self.curl_lout)
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))
        self.df3_host_layout.addWidget(QLabel(" "))

        self.groupbox.setLayout(self.df3_host_layout)
       

#==========================================================================================================
#================================= ================= ======================================================
#==========================================================================================================



        def disableWidget():
            if self.combobox1.currentIndex() == 0:
                self.label1.setText('x component')
                self.label2.setText('y component')
                self.label3.setText('z component')
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(True)
                self.line_edit3.setEnabled(True)
                self.label1.setEnabled(True)
                self.label2.setEnabled(True)
                self.label3.setEnabled(True)
                self.box1.setEnabled(False)
                self.box2.setEnabled(False)
                self.box3.setEnabled(False)
                self.box1.setChecked(False)
                self.box2.setChecked(False)
                self.box3.setChecked(False)

            if self.combobox1.currentIndex() == 1:
                self.label1.setText('Field')
                self.label2.setText(' ')
                self.label3.setText(' ')
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(False)
                self.line_edit3.setEnabled(False)
                self.label1.setEnabled(True)
                self.label2.setEnabled(False)
                self.label3.setEnabled(False)
                self.box1.setEnabled(False)
                self.box2.setEnabled(False)
                self.box3.setEnabled(False)
                self.box1.setChecked(False)
                self.box2.setChecked(False)
                self.box3.setChecked(False)

            
            if self.combobox1.currentIndex() == 2:
                self.label1.setText('dx')
                self.label2.setText('dy')
                self.label3.setText('dz')
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(True)
                self.line_edit3.setEnabled(True)
                self.label1.setEnabled(True)
                self.label2.setEnabled(True)
                self.label3.setEnabled(True)
                self.box1.setEnabled(False)
                self.box2.setEnabled(False)
                self.box3.setEnabled(False)
                self.box1.setChecked(False)
                self.box2.setChecked(False)
                self.box3.setChecked(False)

            if self.combobox1.currentIndex() == 3:
                self.label1.setText('dy ∧ dz')
                self.label2.setText('dz ∧ dx')
                self.label3.setText('dx ∧ dy')
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(False)
                self.line_edit3.setEnabled(False)
                self.label1.setEnabled(True)
                self.label2.setEnabled(True)
                self.label3.setEnabled(True)
                self.box1.setEnabled(True)
                self.box2.setEnabled(True)
                self.box3.setEnabled(True)
                self.box1.setChecked(True)

            if self.combobox1.currentIndex() == 4:
                self.label1.setText('dx ∧ dy ∧ dz')
                self.label2.setText(' ')
                self.label3.setText(' ')
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(False)
                self.line_edit3.setEnabled(False)
                self.label1.setEnabled(True)
                self.label2.setEnabled(False)
                self.label3.setEnabled(False)
                self.box1.setEnabled(False)
                self.box2.setEnabled(False)
                self.box3.setEnabled(False)
                self.box1.setChecked(False)
                self.box2.setChecked(False)
                self.box3.setChecked(False)



        self.f2_btn_grp = QButtonGroup()
        self.f2_btn_grp.addButton(self.box1)
        self.f2_btn_grp.addButton(self.box2)
        self.f2_btn_grp.addButton(self.box3)
        self.f2_btn_grp.setExclusive(True) 



        self.combobox1.currentIndexChanged['QString'].connect(disableWidget)

        def f2_toggler():
            if self.box1.isChecked()==True:
                self.box2.setChecked(False)
                self.box3.setChecked(False)
                self.line_edit1.setEnabled(True)
                self.line_edit2.setEnabled(False)
                self.line_edit3.setEnabled(False)
            if self.box2.isChecked()==True:
                self.box1.setChecked(False)
                self.box3.setChecked(False)
                self.line_edit1.setEnabled(False)
                self.line_edit2.setEnabled(True)
                self.line_edit3.setEnabled(False)
            if self.box3.isChecked()==True:
                self.box2.setChecked(False)
                self.box1.setChecked(False)
                self.line_edit1.setEnabled(False)
                self.line_edit2.setEnabled(False)
                self.line_edit3.setEnabled(True)

        self.box1.toggled.connect(lambda: f2_toggler())
        self.box2.toggled.connect(lambda: f2_toggler())
        self.box3.toggled.connect(lambda: f2_toggler())
        






        self.ui = self.visualization.edit_traits(parent=self, 
                                                 kind='subpanel').control
    


        layout.addWidget(self.ui, 0, 0, 1, 2)
        layout.addWidget(spc, 1, 0)
        layout.addWidget(self.combobox1, 2, 0)


        layout.addWidget(self.label1, 3, 0)
        layout.addLayout(self.sublayout1, 4, 0)


        layout.addWidget(self.label2, 5, 0)
        layout.addLayout(self.sublayout2, 6, 0)


        layout.addWidget(self.label3, 7, 0)
        layout.addLayout(self.sublayout3, 8, 0)

        layout.addWidget(self.groupbox, 0, 2, 1,2)
        layout.addWidget(self.groupbox_ax_param, 1, 1, 8, 1)
        layout.addWidget(self.groupbox_scaling, 1, 2, 8, 1)
        layout.addWidget(self.groupbox_cosmetic, 1, 3, 8, 1)


        layout.setHorizontalSpacing(20)
        

        self.ui.setParent(self)
 

    def clear(self):
        self.visualization.clear()





#===================Change UI based on the dropbox option========================================================


    def dropbox_option_UI_change(self, value):

        if value == 0:
            self.dial_stack_label.setText("Vectors")

        if value == 2:
            self.dial_stack_label.setText("Stacks")


#================================================================================================================






    def create_df3_plot(self):

        if self.combobox1.currentIndex()==2:
            stck_coords, red_balls_data, axes_limits = self.createForm1()
            self.visualization.takePlotParametresF1(stck_coords, red_balls_data, axes_limits)
        elif self.combobox1.currentIndex()==0:
            fld_copms, red_balls_data1, axes_limits1, cmap_vs_clr_idx, clrmap, vecclr, sngclr = self.createVF()
            self.visualization.takePlotParametresVF(fld_copms, red_balls_data1, axes_limits1, cmap_vs_clr_idx, clrmap, vecclr, sngclr)
        elif self.combobox1.currentIndex()==1:
            sc_fld, axes_limits_f0 = self.createForm0()
            self.visualization.takePlotParametresF0(sc_fld, axes_limits_f0)
        elif self.combobox1.currentIndex()==3:
            xg, yg, zg, fx, fy, fz, fx_eqn, fy_eqn, fz_eqn = self.createForm2()
            self.visualization.takePlotParametresF2(xg, yg, zg, fx, fy, fz, fx_eqn, fy_eqn, fz_eqn)
        elif self.combobox1.currentIndex()==4:
            xg3, yg3, zg3, f3, f3_eqn = self.createForm3()
            self.visualization.takePlotParametresF3(xg3, yg3, zg3, f3, f3_eqn)
        else:
            print('kek')
 


    def createForm1(self):

        gridx = np.linspace((float(self.foc_pt_x.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_x.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridy = np.linspace((float(self.foc_pt_y.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_y.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridz = np.linspace((float(self.foc_pt_z.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_z.text())+float(self.range.text())/2),\
                             int(self.pts.text()))

        xg, yg, zg = np.meshgrid(gridx, gridy, gridz)

        fx = xg/np.sqrt(xg**2+yg**2 - zg**2)
        fy = yg/np.sqrt(xg**2+yg**2- zg**2)
        fz = yg/np.sqrt(xg**2+yg**2- zg**2)
        

        fx_eqn = self.line_edit1.text()
        fy_eqn = self.line_edit2.text()
        fz_eqn = self.line_edit3.text()

        form_1 = df3.form_1_3d(xg, yg, zg, fx, fy, fz, scaling=self.dial_stack.value()/1000, sng_scl=self.dial_redball.value()/1000)

        form_1.give_eqn(fx_eqn, fy_eqn, fz_eqn)

        stck_coords, red_balls_data, axes_limits = form_1.plot()



        return stck_coords, red_balls_data, axes_limits
 

    def createForm0(self):

        gridx = np.linspace((float(self.foc_pt_x.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_x.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridy = np.linspace((float(self.foc_pt_y.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_y.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridz = np.linspace((float(self.foc_pt_z.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_z.text())+float(self.range.text())/2),\
                             int(self.pts.text()))

        xg, yg, zg = np.meshgrid(gridx, gridy, gridz)

        f0 = xg/np.sqrt(xg**2+yg**2 - zg**2)

        f0_eqn = self.line_edit1.text()

        form_0 = df3.form_0_3d(xg, yg, zg, f0)

        form_0.give_eqn(f0_eqn)

        sc_field, axes_limits = form_0.plot()



        return sc_field, axes_limits


    def createVF(self, curl_idx = None):

        gridx = np.linspace((float(self.foc_pt_x.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_x.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridy = np.linspace((float(self.foc_pt_y.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_y.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridz = np.linspace((float(self.foc_pt_z.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_z.text())+float(self.range.text())/2),\
                             int(self.pts.text()))

        xg, yg, zg = np.meshgrid(gridx, gridy, gridz)

        fx = 1
        fy = 1
        fz = 1
        

        fx_eqn = self.line_edit1.text()
        fy_eqn = self.line_edit2.text()
        fz_eqn = self.line_edit3.text()

        vf = df3.vector_field3(xg, yg, zg, fx, fy, fz, scaling=self.dial_stack.value()/1000, sing_scl=self.dial_redball.value()/1000)

        vf.give_eqn(fx_eqn, fy_eqn, fz_eqn)

        fld_comps, red_balls_data, axes_limits = vf.plot()

        div = vf.div(at_x = 0, at_y = 0, at_z = 0)
        if type(div) == str:
            self.div_val.setText(str(div))
        else:
            self.div_val.setText('{0:.2f}'.format(div))

        self.div_lbl.setText("Divergence at ({}, {}, {}): ".format(self.foc_pt_x.text(), self.foc_pt_y.text(), self.foc_pt_z.text()))

        if self.vec_cmap_chckbox.isChecked()==True:
            cmap_vs_clr_idx = 0
        if self.vec_clr_chckbox.isChecked()==True:
            cmap_vs_clr_idx = 1

       

        return fld_comps, red_balls_data, axes_limits, cmap_vs_clr_idx, self.cmap_list.currentText(), self.rgb_vec, self.rgb_sng

    
    def createForm2(self):

        gridx = np.linspace((float(self.foc_pt_x.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_x.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridy = np.linspace((float(self.foc_pt_y.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_y.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridz = np.linspace((float(self.foc_pt_z.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_z.text())+float(self.range.text())/2),\
                             int(self.pts.text()))

        xg, yg, zg = np.meshgrid(gridx, gridy, gridz)

        fx = xg/np.sqrt(xg**2+yg**2 - zg**2)
        fy = yg/np.sqrt(xg**2+yg**2- zg**2)
        fz = yg/np.sqrt(xg**2+yg**2- zg**2)
        

        

        if self.box1.isChecked()==True:
            fx_eqn = self.line_edit1.text()
            fy_eqn = '0'
            fz_eqn = '0'

        if self.box2.isChecked()==True:
            fx_eqn = '0'
            fy_eqn = self.line_edit2.text()
            fz_eqn = '0'

        if self.box3.isChecked()==True:
            fx_eqn = '0'
            fy_eqn = '0'
            fz_eqn = self.line_edit3.text()





        return xg, yg, zg, fx, fy, fz, fx_eqn, fy_eqn, fz_eqn


    
    def createForm3(self):

        gridx = np.linspace((float(self.foc_pt_x.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_x.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridy = np.linspace((float(self.foc_pt_y.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_y.text())+float(self.range.text())/2),\
                             int(self.pts.text()))
        gridz = np.linspace((float(self.foc_pt_z.text())-float(self.range.text())/2),\
                            (float(self.foc_pt_z.text())+float(self.range.text())/2),\
                             int(self.pts.text()))

        xg, yg, zg = np.meshgrid(gridx, gridy, gridz)

        f3 = xg/np.sqrt(xg**2+yg**2 - zg**2)
        
        f3_eqn = self.line_edit1.text()

        return xg, yg, zg, f3, f3_eqn







if __name__ == "__main__":

    app = QtGui.QApplication.instance()
 
    container = QtGui.QWidget()
    container.setWindowTitle("DFormPy 3D GUI")

    overlayout = QtGui.QHBoxLayout(container)
    container.setGeometry(0,0,500,500)

    layout = QtGui.QVBoxLayout()
    
 
    mayavi_widget = MayaviQWidget()
 
    button = QtGui.QPushButton('Generate plot')
    button.setMinimumHeight(35)
    button.clicked.connect(mayavi_widget.create_df3_plot)

    
 
    layout.addWidget(mayavi_widget)
    
    layout.addWidget(button)



    button2 = QtGui.QPushButton('Clear canvas')
    button2.move(100,0)
    button2.clicked.connect(mayavi_widget.clear)
    overlayout.addLayout(layout)
    #overlayout.addWidget(button2)
    
 
    container.show()
 
    app.exec_()



