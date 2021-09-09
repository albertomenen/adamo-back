# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:41:35 2019

@author: pjvidal
"""
import copy
import numpy as np
from numpy import linalg as LA
from open3d import *

"""Funcion que calcula los ejes de referencia del cuerpo a partir de su media y su matriz de covarianza.
   Devuelve el angulo de inclinacion vertical y el line_set para su visualizacion. """
def obtain_reference_frame(med,cov):
    
    w, v = LA.eig(cov)
    v[0] = v[0]*np.sqrt(w[0]) 
    v[1] = v[1]*np.sqrt(w[1])
    v[2] = v[2]*np.sqrt(w[2])
    
    #Se ordenan los ejes para que el mayor sea el primero 
    norm_v = LA.norm(v, axis=1)    
    sortidxs = np.argsort(norm_v)
    v_sort = v[sortidxs]
    norm_v_sort = LA.norm(v_sort, axis=1)
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
    return theta, line_set

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
def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    draw_geometries([source_temp, target_temp])
    

def preprocess_point_cloud(pcd, voxel_size):
    #print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = voxel_down_sample(pcd, voxel_size)

    radius_normal = voxel_size * 2
    #print(":: Estimate normal with search radius %.3f." % radius_normal)
    estimate_normals(pcd_down, KDTreeSearchParamHybrid(
            radius = radius_normal, max_nn = 30))

    radius_feature = voxel_size * 5
    #print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = compute_fpfh_feature(pcd_down,
            KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 1000))
    return pcd_down, pcd_fpfh

def prepare_dataset(voxel_size, source, target):
    #print(":: Load two point clouds and disturb initial pose.")
    #trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0],
    #                        [1.0, 0.0, 0.0, 0.0],
    #                        [0.0, 1.0, 0.0, 0.0],
    #                        [0.0, 0.0, 0.0, 1.0]])
    trans_init = np.asarray([[1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0],
                             [0.0, 0.0, 1.0, 0.0],
                             [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    #draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh

def execute_global_registration(
        source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    #print(":: RANSAC registration on downsampled point clouds.")
    #print("   Since the downsampling voxel size is %.3f," % voxel_size)
    #print("   we use a liberal distance threshold %.3f." % distance_threshold)
    
    result = registration_ransac_based_on_feature_matching(
            source_down, target_down, source_fpfh, target_fpfh,
            distance_threshold,
            TransformationEstimationPointToPoint(False), 4,
            [CorrespondenceCheckerBasedOnEdgeLength(0.9),
            CorrespondenceCheckerBasedOnDistance(distance_threshold)],
            RANSACConvergenceCriteria(4000000, 500))
    
    #print(result.fitness)
    
    return result

def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size, result_ransac):
#def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.4
    estimate_normals(source,search_param=KDTreeSearchParamHybrid(radius=0.1,max_nn=30))
    estimate_normals(target,search_param=KDTreeSearchParamHybrid(radius=0.1,max_nn=30))
    #orient_normals_to_align_with_direction(source)
    #orient_normals_to_align_with_direction(target)
    #print(":: Point-to-plane ICP registration is applied on original point")
    #print("   clouds to refine the alignment. This time we use a strict")
    #print("   distance threshold %.3f." % distance_threshold)
    result = registration_icp(source, target, distance_threshold,
            result_ransac.transformation,
            TransformationEstimationPointToPlane(),
            ICPConvergenceCriteria(0.00000001, 0.00000001, 40000))
    return result

def calcular_offset(color_image1, depth_image1, color_image2,depth_image2, intrinsics1, intrinsics2, depth_scale1, depth_scale2, treatment_points,gui_active):

    """ Se generan las imagenes RGDB a partir de los datos recibidos."""
    color_raw1 = Image(color_image1)
    depth_raw1 = Image(depth_image1)
    color_raw2 = Image(color_image2)
    depth_raw2 = Image(depth_image2)
    
    rgbd_image1 = create_rgbd_image_from_color_and_depth(color_raw1, depth_raw1)
    rgbd_image2 = create_rgbd_image_from_color_and_depth(color_raw2, depth_raw2)
    
    #mat_pos_ini = [[1,  0,  0, 0],
    #               [0, -1,  0, 0],
    #               [0,  0, -1, 0],
    #               [0,  0,  0, 1]] 
    
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
    #pcd_trat.transform(giro_x(np.pi))
   
    #pcd_trat.transform(giro_z(-np.pi/2))
    #rx = np.rad2deg(50)                    
    #T_rot =   np.matrix([[1        , 0              ,0           ,  0],
    #                   [0        , np.cos(rx)     ,-np.sin(rx) ,  0],
    #                   [0        , np.sin(rx)     ,np.cos(rx)  ,  0],
    #                   [0        , 0              ,0           ,  1]])     
    
    #pcd1_raw.transform(T_rot)
    #pcd2_raw.transform(T_rot)
    #pcd_trat.transform(T_rot)
    
    
    if gui_active == True:
        ejes_ref_camara = obtain_axis() #ejes del sistema de coordenadas de la camara
        pcd_trat.paint_uniform_color([1, 0, 0]) # Primeros eb rojo
        draw_geometries([pcd_trat,ejes_ref_camara,pcd1_raw])   

    
    """Se filtran los puntos para quedarnos con el volumen de la espalda"""
    xyz_load1 = np.asarray(pcd1_raw.points)
    xyz_load2 = np.asarray(pcd2_raw.points)
    
        
    #h_max = np.max(pcd_trat_girados[:,2]); #Para filtrar la pointcloud se usan los propios puntos del tratamiento.
    #h_min = h_max - 0.1
    
    puntos1 = point_cloud_filter(xyz_load1)
    puntos2 = point_cloud_filter(xyz_load2)
    
    target1 = PointCloud()
    target1.points = Vector3dVector(puntos2) 
    source1 = PointCloud()
    source1.points = Vector3dVector(puntos1)
    
   
    """ALINEAMIENTO""" 
    voxel_size = 0.01 # means 5cm for the dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = \
            prepare_dataset(voxel_size, source1, target1)
    
    result_ransac = execute_global_registration(source_down, target_down,
            source_fpfh, target_fpfh, voxel_size)
    print("Resultado RANSAC")
    print(result_ransac)
    
    """ Si el error cuadratico medio de RANSAC es mayor de 0.01"""
    if result_ransac.inlier_rmse > 0.01:
        print("No se han alineado bien los volumenes con RANSAC.")
        return False, 0
    
    if gui_active == True:
        draw_registration_result(source_down, target_down,
                                    result_ransac.transformation)
    
    result_icp = refine_registration(source, target,
            source_fpfh, target_fpfh, voxel_size, result_ransac)
    #result_icp = refine_registration(source, target,
    #        source_fpfh, target_fpfh, voxel_size)
    print("Result ICP: ")
    print(result_icp)
    
    """ Si el error cuadratico medio de ICP es mayor de 0.01"""
    if result_icp.inlier_rmse > 0.01:
        print("No se han alineado bien los volumenes con ICP.")
        return False, 0
    
    
    if gui_active == True:
        source_temp = copy.deepcopy(source)
        target_temp = copy.deepcopy(target)
        source_temp.paint_uniform_color([1, 0.706, 0])
        target_temp.paint_uniform_color([0, 0.651, 0.929])
        source_temp.transform(result_icp.transformation)
        draw_geometries([source_temp, target_temp])
        
    
    pcd_trat_transf = PointCloud()
    pcd_trat_transf = copy.deepcopy(pcd_trat)
    
    
    # Se aplica la transformacion encontrada por el metodo ICP
    pcd_trat_transf.transform(result_icp.transformation)
    
    # Se transforman los puntos para que coincidan con las coordenadas de la camara
    #pcd_trat.transform(T_rot.T)
    #pcd_trat_transf.transform(T_rot.T)
    
    # Se restan las pcd para calcular el offset
    #p_trat = np.asarray(pcd_trat.points)
    p_trat_transf = np.asarray(pcd_trat_transf.points)
    offset = p_trat_transf - p_trat
    
    
    
    """Si el offset tiene la forma deseada"""
    if offset.shape == (len(p_trat),3):
        status = True
    else:
        status = False
                        
    
    """"""""""""""""VISUALIZACION"""""""""""""""""
    if gui_active == True:
        pcd_trat.paint_uniform_color([1, 0, 0]) # Primeros eb rojo
        pcd_trat_transf.paint_uniform_color([0, 0, 1]) #
        # Se crea el lineset para unir cada punto
        points = []
        lines = []
        points[0:len(p_trat)] = p_trat
        points[len(p_trat):2*len(p_trat)-1] = p_trat+offset
        for i in range(len(p_trat)):
            lines.append([i,i+len(p_trat)])
        
        colors = [[0,0,255]]
        line_set = LineSet()
        line_set.points = Vector3dVector(points)
        line_set.lines = Vector2iVector(lines)
        line_set.colors = Vector3dVector(colors)
        
        source1.paint_uniform_color([1, 1, 0])
        target1.paint_uniform_color([0, 1, 1])
    
        draw_geometries([pcd_trat,pcd_trat_transf,source1, target1 , line_set])
        
        #draw_geometries([pcd1_raw,pcd_trat])
        draw_geometries([pcd2_raw,pcd_trat_transf])
    
    """"""""""""""""FIN DE LA VISUALIZACION"""""""""""""""""
    
    return status, offset;

