# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:41:35 2019

@author: pjvidal
"""
import copy
import numpy as np
from numpy import linalg as LA
from open3d import *
from scipy.signal import argrelextrema

"""Funcion que calcula los ejes de referencia del cuerpo a partir de su media y su matriz de covarianza.
   Devuelve el angulo de inclinacion vertical y el line_set para su visualizacion. """
def obtain_reference_frame(med,cov):
    
    w, v = LA.eig(cov)
    v[0] = v[0]*np.sqrt(w[0]) 
    v[1] = v[1]*np.sqrt(w[1])
    v[2] = v[2]*np.sqrt(w[2])
    
    if LA.norm(v[2]) > LA.norm(v[0]) or LA.norm(v[2]) > LA.norm(v[1]):
        return 0,0, True
    #Se ordenan los ejes para que el mayor sea el primero 
    norm_v = LA.norm(v, axis=1)    
    sortidxs = np.argsort(norm_v)
    v_sort = v[sortidxs]
    #norm_v_sort = LA.norm(v_sort, axis=1)
    v = np.flip(v_sort,axis = 0)
   
    if (v[0,1]) < 0: # Si el eje mayor apunta hacia abajo:
        v[0] = (-1) * v[0]  # Se le da la vuelta
        v[1] = (-1) * v[1]  # Se le da la vuelta

    
    v[0] = v[0] + med
    v[1] = v[1] + med
    v[2] = v[2] + med
    
    
    points = [med,v[0],v[1],v[2]]
    lines = [[0,1],[0,2],[0,3]]
    #colors = [[0, 0, 0] for i in range(len(lines))]
    colors = [[0,0,255],[0,255,0],[255,0,0]]
    line_set = LineSet()
    line_set.points = Vector3dVector(points)
    line_set.lines = Vector2iVector(lines)
    line_set.colors = Vector3dVector(colors)
    theta = np.rad2deg(np.arctan((v[0,1]-med[1])/(v[0,0]-med[0])))
    
    return theta, line_set, False


def obtain_reference_frame_2(med,cov):
    w, v = LA.eig(cov)
    v[0] = v[0]*np.sqrt(w[0]) 
    v[1] = v[1]*np.sqrt(w[1])
    v[2] = v[2]*np.sqrt(w[2])
    
    if LA.norm(v[2]) > LA.norm(v[0]) or LA.norm(v[2]) > LA.norm(v[1]):
        return 0,0, True
    
    #Se ordenan los ejes para que el mayor sea el primero 
    norm_v = LA.norm(v, axis=1)    
    sortidxs = np.argsort(norm_v)
    v_sort = v[sortidxs]
    norm_v_sort = LA.norm(v_sort, axis=1)
    v = np.flip(v_sort,axis = 0)
   
    if (v[0,1]) < 0: # Si el eje mayor apunta hacia abajo:
        v[0] = (-1) * v[0]  # Se le da la vuelta
        v[1] = (-1) * v[1]  # Se le da la vuelta
        
    v[0] = v[0] + med #Vector director mayor
    v[1] = v[1] + med
    v[2] = v[2] + med
    
    theta = 90-np.rad2deg(np.arctan2((v[0,1]-med[0]),(v[0,0]-med[0])))
    
    if np.abs(theta) > 20:
        return 0, 0, True
    
    points = [med,v[0],v[1],v[2]]
    lines = [[0,1],[0,2],[0,3]]
    #colors = [[0, 0, 0] for i in range(len(lines))]
    colors = [[0,0,255],[0,255,0],[255,0,0]]
    line_set = LineSet()
    line_set.points = Vector3dVector(points)
    line_set.lines = Vector2iVector(lines)
    line_set.colors = Vector3dVector(colors)
    
    return theta, line_set, False


"""Funcion que recorta la nube de puntos para quedarse con la espalda del paciente"""
def point_cloud_filter(xyz_load,h_min=None,h_max=None):
    
    corte_horizontal_izq = 0.35  # izquierda vista desde arriba
    corte_horizontal_dch = 0.35 # derecha vista desde arriba
    #corte_vertical = 0.40 # Distancia fija del mueble del robot
    puntos =  xyz_load[(xyz_load[:,2] != 0) ] #Puntos en el origen 
    
    """ Crop point cloud """    
    puntos = puntos[(puntos[:,0] > - corte_horizontal_dch)] #Quita los laterales de la camilla
    puntos = puntos[(puntos[:,0] < + corte_horizontal_izq)] #Quita los laterales de la camilla
    
    #puntos = puntos[(puntos[:,1] > - corte_vertical)] #Quita el cabezal del robot si llegara a verse
    if h_max != None and h_min != None:
        puntos =  puntos[(puntos[:,2] < h_max)] # Los menores que h_max
        puntos =  puntos[(puntos[:,2] > h_min)] # Los mayores que h_min
   
    if h_max == None or h_min == None:
        puntos = puntos[(puntos[:,2] < np.mean(puntos[:,2]))] #Camilla
        #puntos = puntos[(puntos[:,2] < np.mean(puntos[:,2]))] #Espalda
    #puntos1 = puntos1[(puntos1[:,2] > (puntos1[:,2].max()-0.15))]
    #puntos = puntos[(puntos[:,2] > np.mean(puntos[:,2]))] #Por encima de la camilla
    
    """ Filter Outliers """
    puntos = puntos[(puntos[:,0] < np.mean(puntos[:,0]) + 2*np.std(puntos[:,0]))] # Si hay outliers en los laterales los quita
    puntos = puntos[(puntos[:,0] > np.mean(puntos[:,0]) - 2*np.std(puntos[:,0]))]
    puntos = puntos[(puntos[:,1] < np.mean(puntos[:,1]) + 2*np.std(puntos[:,1]))] # Si hay outliers en los longitudinales los quita
    puntos = puntos[(puntos[:,1] > np.mean(puntos[:,1]) - 2*np.std(puntos[:,1]))] 
    puntos = puntos[(puntos[:,2] < np.mean(puntos[:,2]) + 2*np.std(puntos[:,2]))] # Si hay outliers en la altura los quita
    puntos = puntos[(puntos[:,2] > np.mean(puntos[:,2]) - 2*np.std(puntos[:,2]))] 

    #puntos = puntos[(puntos[:,2] > np.mean(puntos[:,2]))] #Espalda
    
    return puntos


def desplazar(x,y,z):
    mat_desp =[[1                 , 0                  ,0,  x],
               [0                 , 1                  ,0,  y],
               [0                 , 0                  ,1,  z],
               [0                 , 0                  ,0,  1]]
    return mat_desp

def giro_x(rx):
    mat_desp =[[1        , 0              ,0           ,  0],
               [0        , np.cos(rx)     ,-np.sin(rx) ,  0],
               [0        , np.sin(rx)     ,np.cos(rx)  ,  0],
               [0        , 0              ,0           ,  1]]
    return mat_desp

def giro_y(ry):
    mat_desp =[[np.cos(ry)      , 0      ,np.sin(ry)   ,  0],
               [0               , 1      ,0            ,  0],
               [-np.sin(ry)     , 0      ,np.cos(ry)   ,  0],
               [0               , 0      ,0            ,  1]]
    return mat_desp

def giro_z(rz):
    mat_desp =[[np.cos(rz)        ,-np.sin(rz)         ,0,  0],
               [np.sin(rz)        , np.cos(rz)         ,0,  0],
               [0                 , 0                  ,1,  0],
               [0                 , 0                  ,0,  1]]
    return mat_desp

def obtain_axis():
    points = [[0,0,0],[0.1,0,0],[0,0.1,0],[0,0,0.1]]
    lines = [[0,1],[0,2],[0,3]]
    #colors = [[0, 0, 0] for i in range(len(lines))]
    colors = [[255,0,255],[0,255,0],[0,0,255]]
    line_set = LineSet()
    line_set.points = Vector3dVector(points)
    line_set.lines = Vector2iVector(lines)
    line_set.colors = Vector3dVector(colors)
    return line_set

def find_contour(puntos, paso): 
    for i in range(int(min(puntos[:,1])*paso),int(paso*max(puntos[:,1]))):
        
        body_slice = puntos[np.round(puntos[:,1],3) == (i/paso)]
        
        contour_slice = np.ndarray(shape = (2, 3))
        if len(body_slice[:,0]) > 1:
            contour_slice[0] = body_slice[body_slice[:,0] == min(body_slice[:,0])]
            contour_slice[1] = body_slice[body_slice[:,0] == max(body_slice[:,0])]
        
        if i == int(min(puntos[:,1])*paso):# Primer bucle
            array_body_width = np.ndarray(shape = (1,1))
            contour_slices = np.ndarray(shape = (2,3))
            contour_slices[0] = contour_slice[0]
            contour_slices[1] = contour_slice[1]
            if len(body_slice[:,0]) > 1:
                array_body_width = max(body_slice[:,0]) - min(body_slice[:,0])
           
        if len(body_slice[:,0]) > 1:
            array_body_width = np.append(array_body_width, max(body_slice[:,0])-min(body_slice[:,0]))
            
            contour_slices = np.append(contour_slices,np.array(contour_slice), axis = 0)
        
    return contour_slices,array_body_width

"""Funcion que busca los puntos pertenecientes a los hombros calculando la desviaciontipica a lo largo del cuerpo
y buscando el punto medio de esta desviacion."""
def find_features(contorno, array_body_width, cuerpo, paso):

    global pts_cuello
    global pts_cuello_filtrados
    if len(array_body_width) <= 1 or len(contorno) <= 1:
        return 0,0,0, False
    
    minimos_locales = array_body_width[argrelextrema(array_body_width, np.less)[0]]
    #print("minimos_locales: ",minimos_locales)
    if len(minimos_locales) < 1:
        return 0,0,0, False
    elif len(minimos_locales) == 1:
        distancia_cuello_minima = minimos_locales
    else:
        distancia_cuello_minima = min(minimos_locales)
        
    pts_cuello = contorno[np.round(contorno[:,0],1) == np.round(distancia_cuello_minima/2, 1)]
    pto_medio = np.mean(pts_cuello[:,1])
    
    pts_cuello_filtrados = pts_cuello[pts_cuello[:,1] < pto_medio+np.std(pts_cuello[:,1])*2]
    pts_cuello_filtrados = pts_cuello[pts_cuello[:,1] > pto_medio-np.std(pts_cuello[:,1])*2]
    #puntos_cuello = cuerpo[np.logical_and(cuerpo[:,1] < pto_medio + 0.1, cuerpo[:,1] > pto_medio - 0.01)]
    
    ptos_cabeza = cuerpo[cuerpo[:,1] < pto_medio]

    tamano_ventana = 10
    array_std_desv = []
    array_mean = []
    for i in range(int(min(contorno[:,1])*paso),int(max(contorno[:,1])*paso)):
        contour_slice = contorno[np.logical_and(np.round(contorno[:,1],3) > ((i-tamano_ventana)/paso), np.round(contorno[:,1],3) < ((i+tamano_ventana)/paso))]
        array_std_desv.append(np.std(contour_slice[:,0]))
        array_mean.append(np.mean(contour_slice[:,0], axis = 0))
    
    hombros_id = np.where(np.logical_and(array_std_desv <= np.mean(array_std_desv)+0.01 , array_std_desv >= np.mean(array_std_desv)-0.01))
    #print("Id puntos hombros", hombros_id[0])
    if len(hombros_id[0]) <= 1 :
        return 0,0,0, False
        
    hombros_id = hombros_id[0][0]   
     
    minimo = int(min(contorno[:,1])*paso)
    ptos_hombros = contorno[np.logical_and(np.round(contorno[:,1],3) > (((minimo+hombros_id)-tamano_ventana)/paso), np.round(contorno[:,1],3) < (((minimo+hombros_id)+tamano_ventana)/paso))]

    return ptos_hombros,ptos_cabeza,pts_cuello_filtrados, True

def calcular_offset(color_image1, depth_image1, color_image2,depth_image2, intrinsics1, intrinsics2, depth_scale1, depth_scale2, treatment_points):

    """ Se generan las imagenes RGDB a partir de los datos recibidos."""
    color_raw1 = Image(color_image1)
    depth_raw1 = Image(depth_image1)
    color_raw2 = Image(color_image2)
    depth_raw2 = Image(depth_image2)

    print('aqui')
    rgbd_image1 = create_rgbd_image_from_color_and_depth(color_raw1, depth_raw1)
    rgbd_image2 = create_rgbd_image_from_color_and_depth(color_raw2, depth_raw2)
    print('aqui')
    print(rgbd_image1)
    mat_pos_ini = [[1,  0,  0, 0],
                   [0, -1,  0, 0],
                   [0,  0, -1, 0],
                   [0,  0,  0, 1]] 
    
    """NUBE PUNTOS CREAR TRATAMIENTO"""
    pcd1_raw = PointCloud()        
    pcd1_raw = create_point_cloud_from_rgbd_image(rgbd_image1, PinholeCameraIntrinsic(intrinsics1.width, intrinsics1.height, intrinsics1.fx, intrinsics1.fy, intrinsics1.ppx, intrinsics1.ppy))
    #pcd1_raw.transform(mat_pos_ini)
    """NUBE PUNTOS APLICAR TRATAMIENTO"""
    pcd2_raw = PointCloud()        
    pcd2_raw = create_point_cloud_from_rgbd_image(rgbd_image2, PinholeCameraIntrinsic(intrinsics2.width, intrinsics2.height, intrinsics2.fx, intrinsics2.fy, intrinsics2.ppx,intrinsics2.ppy))
    #pcd2_raw.transform(mat_pos_ini)
    
    
    
        
    """PUNTOS DEL TRATAMIENTO"""
    """Estos puntos estan definidos en el sistema de coordenadas de la camara"""
    p_trat = treatment_points
        
    pcd_trat = PointCloud()
    pcd_trat.points = Vector3dVector(p_trat)
    
    axis = obtain_axis()
    """Se filtran los puntos para quedarnos con el volumen de la espalda"""
    xyz_load1 = np.asarray(pcd1_raw.points)
    xyz_load2 = np.asarray(pcd2_raw.points)
    pcd_trat_girados = np.asarray(pcd_trat.points)
    
    puntos1 = point_cloud_filter(xyz_load1)
    puntos2 = point_cloud_filter(xyz_load2)
    
    """Se obtienen los ejes principales de cada volumen de la espalda en el objeto frame"""
    """ y el angulo de inclinacion del eje vertical en theta"""
    """Se guardan los puntos filtrados en una nueva pointCloud."""
    pcd1 = PointCloud()
    pcd1.points = Vector3dVector(puntos1) 
    med1, cov1 = geometry.compute_point_cloud_mean_and_covariance(pcd1)
    theta1,frame1,err1 = obtain_reference_frame(med1, cov1)
    
    pcd2 = PointCloud() 
    pcd2.points = Vector3dVector(puntos2) 
    med2, cov2 = geometry.compute_point_cloud_mean_and_covariance(pcd2)
    theta2,frame2,err2 = obtain_reference_frame(med2, cov2)

    if err1 or err2: 
        print("Se han calculado mal los ejes principales.")
        return False, 0

    med_p_trat, cov2_p_trat = geometry.compute_point_cloud_mean_and_covariance(pcd_trat)
    
        
    if theta1 < 0:
        theta1 = theta1 + 180
    if theta2 < 0:
        theta2 = theta2 + 180   

    theta_giro_z = np.deg2rad(theta2-theta1) # angulo de giro entre el 2 y el 1 en el ejez
    
    pxyz = med2-med1
    
    print("Offset del point cloud")
    print(pxyz)
    print("Angulo de giro relativo entre los dos: ")
    print(np.rad2deg(theta_giro_z))
    if np.rad2deg(theta_giro_z) > 30:
        return False, 0
    
    
    """**********************Calculo del offset vertical**********************"""
    """Se busca una referencia fija entre ambos volumenes como los hombros o el cuello."""
    pcd1.paint_uniform_color([0, 1, 0.706]) #Verde el cuerpo 1
    pcd2.paint_uniform_color([1, 0.706, 0]) 
    
    theta1_c, frame1_c, err1 = obtain_reference_frame_2(med1, cov1) 
    theta2_c,frame2_c, err2 = obtain_reference_frame_2(med2, cov2)
    print("Angulo 1: ",theta1_c)
    print("Angulo 2: ",theta2_c)
    
    if err1 or err2: 
        print("El angulo de giro del paciente en la camilla es mayor a 20 grados o la covarianza no es representativa.")
        return False, 0

    
    """Se llevan los volumenes al origen 0,0,0"""
    pcd1.transform(desplazar(-med1[0],-med1[1],-med1[2]))
    pcd1.transform(giro_z(np.deg2rad(theta1_c)))
    
    pcd2.transform(desplazar(-med2[0],-med2[1],-med2[2]))
    pcd2.transform(giro_z(np.deg2rad(theta2_c)))
    
    """Se obtiene el contorno y se detecta el cuello"""
    paso = 500
    puntos1 =np.asarray(pcd1.points)
    contorno1, array_body_width1 = find_contour(puntos1,paso)
    ptos_hombros1,ptos_cabeza1,pts_cuello_filtrados1, err1 = find_features(contorno1, array_body_width1, puntos1,paso)

    puntos2 = np.asarray(pcd2.points)
    contorno2, array_body_width2 = find_contour(puntos2,paso)
    ptos_hombros2,ptos_cabeza2,pts_cuello_filtrados2, err2 = find_features(contorno2, array_body_width2, puntos2,paso)
    
    if err1 != True or err2 != True:
        print("No se han podido encontrar los hombros")
        return False, 0
    
    """Se obtiene la media y la covarianza de los puntos del cuello"""
    pcd_features1 = PointCloud()
    pcd_features1.points = Vector3dVector(ptos_hombros1) 
    med_cuello1, cov_cuello1 = geometry.compute_point_cloud_mean_and_covariance(pcd_features1)
    
    pcd_features2 = PointCloud()
    pcd_features2.points = Vector3dVector(ptos_hombros2) 
    med_cuello2, cov_cuello2 = geometry.compute_point_cloud_mean_and_covariance(pcd_features2)
    
    
    print("med_cuello1: ", med_cuello1)
    print("med_cuello2: ", med_cuello2)

    
    pxyz_c = (med_cuello2-med_cuello1)
    
    print("Desplazamiento tronco: ", pxyz)
    print("Desplazamiento cuello: ", pxyz_c)
    

    pcd1.transform(desplazar(med1[0],med1[1],med1[2]))
    pcd1.transform(giro_z(-np.deg2rad(theta1_c)))
    pcd_features1.transform(desplazar(med1[0],med1[1],med1[2]))
    pcd_features1.transform(giro_z(-np.deg2rad(theta1_c)))
        
    pcd_features2.transform(desplazar(med2[0],med2[1],med2[2]))
    pcd_features2.transform(giro_z(-np.deg2rad(theta2_c)))
    pcd2.transform(desplazar(med2[0],med2[1],med2[2]))
    pcd2.transform(giro_z(-np.deg2rad(theta2_c)))

    
    """ALINEACION"""
    """ Se busca la transformacion necesaria para alinear el volumen1 con el volumen2
        esta transformacion será la misma que la necesaria para mover los puntos del 
        tratamiento de un volumen a otro."""
    #Se copian los puntos del tratamiento para desplazarlos y calcular el offset
    pcd_trat_off = copy.deepcopy(pcd_trat)
    
    #Se colocan en el origen
    pcd_trat_off.transform(desplazar(-med1[0],-med1[1],-med1[2])) #Antes era med1

    #Se alinean los puntos 1 con los puntos2

    #pcd_trat_off.transform(desplazar(pxyz_c[0],pxyz_c[1],pxyz_c[2]))
    
    pcd_trat_off.transform(giro_z(theta_giro_z))
    
    #Se colocan donde estaban antes
    pcd_trat_off.transform(desplazar(med1[0],med1[1],med1[2]))
    
    #Se mueven los puntos1 hacia los puntos2
    pcd_trat_off.transform(desplazar(pxyz[0],pxyz[1]+pxyz_c[1],pxyz[2]))
    
    
    # Se transforman los puntos para que coincidan con las coordenadas de la camara
    #pcd_trat.transform(T_rot.T)
    #pcd_trat_off.transform(T_rot.T)
    
    
    xyz_load_trat1 = np.asarray(pcd_trat.points)
    xyz_load_trat2 = np.asarray(pcd_trat_off.points)
    
    """El offset será la diferencia entre cada punto aplicado a los dos volumenes"""
    offset = xyz_load_trat2-xyz_load_trat1 
    
    #print(offset)
    #offset[:,1] = offset_vertical
    #print("Calculo de offset despues de la correccion vertical: ")
    #print(offset)
    
    """"""""""""""""FIN DE LA VISUALIZACION"""""""""""""""""
    
    return True, offset

