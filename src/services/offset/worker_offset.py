# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:52:10 2019

@author: pjvidal
"""
import base64
import io
from io import BytesIO
from math import floor, ceil

from PIL import Image

import numpy as np
import cv2

from . import point_cloud_procces_offset as pcpo
from . import point_cloud_procces_offset_v2 as pcpo2

# ----------------------------------------------------------------------

msgImagenes = '''{ 
                        "firstImage": {
                                       "idColor" : "https://i.ibb.co/xj4vDyT/color-image1.png",
                                       "idDepth" : "https://i.ibb.co/S6CYjM0/depth-image1.png",
                                       "width" : "640",
                                       "height" : "480",
                                       "ppx" : "326.79736328125",
                                       "ppy" : "239.5101776123047",
                                       "fx" : "614.009521484375",
                                       "fy" : "614.193603515625",
                                       "model" : "None", 
                                       "coeff" : "[0, 0, 0, 0, 0]",
                                       "depthScale" : 0.001
                                       },
                        "lastImage": {
                                       "idColor" : "https://i.ibb.co/brJMsdT/color-image2.png",
                                       "idDepth" : "https://i.ibb.co/5hfr5mR/depth-image2.png",
                                       "width" : "640",
                                       "height" : "480",
                                       "ppx" : "326.79736328125",
                                       "ppy" : "239.5101776123047",
                                       "fx" : "614.009521484375",
                                       "fy" : "614.193603515625",
                                       "model" : "None", 
                                       "coeff" : "[0, 0, 0, 0, 0]",
                                       "depthScale" : 0.001
                                       },
                        "points": [
                                        {
                                          "pressure": 6,
                                          "duration": 5,
                                          "gradual": true,
                                          "x": -0.76,
                                          "y": -0.09,
                                          "z": -0.01,
                                          "rx": 0,
                                          "ry": 0,
                                          "rz": 0,
                                          "height": 11
                                        }, 
                                        {
                                          "pressure": 6,
                                          "duration": 5,
                                          "gradual": true,
                                          "x": -0.78,
                                          "y": -0.01,
                                          "z": -0.01,
                                          "rx": 0,
                                          "ry": 0,
                                          "rz": 0,
                                          "height": 0
                                        },
                                         {
                                          "pressure": 6,
                                          "duration": 5,
                                          "gradual": true,
                                          "x": -0.91,
                                          "y": -0.03,
                                          "z": -0.01,
                                          "rx": 0,
                                          "ry": 0,
                                          "rz": 0,
                                          "height": 12
                                        }
                                      ]
                        }'''


################################### CLASES ###################################
class intrinsics_params:
    def __init__(self, width, height, ppx, ppy, fx, fy, model, coeff):
        self.width = int(width)
        self.height = int(height)
        self.ppx = float(ppx)
        self.ppy = float(ppy)
        self.fx = float(fx)
        self.fy = float(fy)
        self.model = model
        self.coeff = coeff


class states:
    def __init__(self, pending=None, failed=None, working=None, finished=None, canceled=None, error=None, expired=None):
        self.pending = 'pending'  # La solicitud ha sido recibida por el Back Sam y se ha insertado en SNS correctamente. Está lista para ser ejecutada.
        self.failed = 'failed'  # La solucitud no se ha podido insertar en SNS debido a algún problema de conexión.
        self.working = 'working'  # El worker esta trabajando en la petición.
        self.finished = 'finished'  # El worker ha finalizado su tarea, y el resultado está listo para ser obtenido.
        self.canceled = 'canceled'  # La tarea ha sido cancelada.
        self.error_proximidad = 'out_of_range'
        self.error = 'error'  # Se ha producido un error en el calculo del offset por parte del worker
        self.expired = 'expired'  # Cuando la petición ha superado el timeout indicado y no ha sido procesada por ningún worker.


def getI420FromBase64(codec):
    byte_data = base64.b64decode(codec)
    image_data = BytesIO(byte_data)
    return Image.open(image_data)

################################### FUNCIONES ###################################
#def image_base64_to_numpy_array_urllib(image_64, tipo):
#    # global resp
#    # global resp_byte_array
#    # global mutable_byte_array
#    # global imageBinaryBytes
#    # global imageStream
#    # global imageFile
#    # global imagen_p
#    # global opencvImage
#    ## read as HTTPResponse
#    # resp = urllib.urlopen(url)
#    ## read as 1D bytearray
#    # resp_byte_array = resp.read()
#    image = getI420FromBase64(image_64)
#    ## returns a bytearray object which is a mutable sequence of integers in the range 0 <=x< 256
#
#    # print(mutable_byte_array)
#    ## read as unsigned integer 1D numpy array
#    if tipo == "color":
#        image = np.asarray(image, dtype="uint8")
#        ## To decode the 1D image array into a 2D format with RGB color components we make a call to cv2.imdecode
#        #image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#    if tipo == "depth":
#        # imageBinaryBytes = resp_byte_array
#        # imageStream = io.BytesIO(imageBinaryBytes)
#        # imageFile = Image.open(imageStream)
#        image = np.asarray(image, dtype="uint16")
#    # return the image
#    return image



def image_url_to_numpy_array_urllib(image_bites, tipo):
    # resp
    # resp_byte_array
    # mutable_byte_array
    # imageBinaryBytes
    # imageStream
    # imageFile
    # imagen_p
    # opencvImage
    ## returns a bytearray object which is a mutable sequence of integers in the range 0 <=x< 256
    array_bytes = base64.b64decode(image_bites)
    mutable_byte_array = bytearray(array_bytes)

    # print(mutable_byte_array)
    ## read as unsigned integer 1D numpy array
    if tipo == "color":
        image = np.asarray(mutable_byte_array, dtype="uint8")
        ## To decode the 1D image array into a 2D format with RGB color components we make a call to cv2.imdecode
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if tipo == "depth":
        imageBinaryBytes = array_bytes
        imageStream = io.BytesIO(imageBinaryBytes)
        imageFile = Image.open(imageStream)
        opencvImage = np.asarray(imageFile, dtype="uint16")
        imagen_p = opencvImage[:, :, 1] << 8 | opencvImage[:, :, 0]
        # imagen_p = opencvImage
        image = imagen_p
    # return the image
    return image

"""Se reciven los datos necesarios para el calculo del offset y el id en la cola, se hace un long poll cada dos segundos:"""


def json_to_data(response):
    color_image1 = image_url_to_numpy_array_urllib(response['firstImage']['idColor'], "color")
    print("Se descarga im_Color1")
    depth_image1 = image_url_to_numpy_array_urllib(response['firstImage']['idDepth'], "depth")
    print("Se descarga im_Depth1")
    color_image2 = image_url_to_numpy_array_urllib(response['lastImage']['idColor'], "color")
    print("Se descarga im_Color2")
    depth_image2 = image_url_to_numpy_array_urllib(response['lastImage']['idDepth'], "depth")
    print("Se descarga im_Depth2")

    x_crop_l = floor((color_image1.shape[0] - 480) / 2)
    x_crop_r = x_crop_l + 480
    y_crop_l = floor((color_image1.shape[1] - 640) / 2)
    y_crop_r = y_crop_l + 640
    color_image1 = color_image1[y_crop_l:y_crop_r, x_crop_l:x_crop_r]
    # color_image1 = cv2.resize(color_image1, (480, 640))

    color_image2 = color_image2[y_crop_l:y_crop_r, x_crop_l:x_crop_r]
    # color_image2 = cv2.resize(color_image2, (480, 640))

    depth_image1 = depth_image1[y_crop_l:y_crop_r, x_crop_l:x_crop_r]
    # depth_image1 = cv2.resize(depth_image1, (480, 640))

    depth_image2 = depth_image2[y_crop_l:y_crop_r, x_crop_l:x_crop_r]
    # depth_image2 = cv2.resize(depth_image2, (480, 640))

    color_image1 = cv2.rotate(color_image1, cv2.cv2.ROTATE_90_CLOCKWISE)
    color_image2 = cv2.rotate(color_image2, cv2.cv2.ROTATE_90_CLOCKWISE)
    depth_image1 = cv2.rotate(depth_image1, cv2.cv2.ROTATE_90_CLOCKWISE)
    depth_image2 = cv2.rotate(depth_image2, cv2.cv2.ROTATE_90_CLOCKWISE)

    intrinsics1 = intrinsics_params(response['firstImage']['width'], response['firstImage']['height'],
                                    response['firstImage']['ppx'], response['firstImage']['ppy'],
                                    response['firstImage']['fx'], response['firstImage']['fy'],
                                    response['firstImage']['model'], response['firstImage']['coeff'])

    intrinsics2 = intrinsics_params(response['lastImage']['width'], response['lastImage']['height'],
                                    response['lastImage']['ppx'], response['lastImage']['ppy'],
                                    response['lastImage']['fx'], response['lastImage']['fy'],
                                    response['lastImage']['model'], response['lastImage']['coeff'])
    depth_scale1 = response['firstImage']['depthScale']
    depth_scale2 = response['lastImage']['depthScale']

    points = response['points']

    # return response['id'], color_image1, depth_image1, color_image2, depth_image2
    return color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2, depth_scale1, depth_scale2, points


def validate_points(p_trat_r, offset_r):
    radio = 0.9
    p_trat_off_r = p_trat_r + offset_r
    validar = np.linalg.norm(p_trat_off_r, axis=1) < radio
    if len(validar[validar == False]) > 0:
        return False

    return True


def str2bool(string_c):
    if string_c == "True":
        return True
    elif string_c == "False":
        return False


def areTheyParallel(offset, n_points):
    for i in range(n_points):
        for j in range(n_points):
            if i != j:
                crossProduct = np.linalg.norm(np.cross(offset[i], offset[j]))
                if np.sqrt(crossProduct ** 2) > 0.01:
                    return False
    return True


def get_offset(images_to_offset):
    color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2, depth_scale1, depth_scale2, treatment_points = json_to_data(
        images_to_offset)

    print(intrinsics1.height, intrinsics1.width)
    print(intrinsics2.height, intrinsics2.width)
    print(color_image1.shape)
    print(depth_image1.shape)
    print(color_image2.shape)
    print(depth_image2.shape)

    if color_image1.shape != (480, 640, 3):
        raise Exception("The first color image has not been received")
    elif depth_image1.shape != (480, 640):
        raise Exception("The first depth image has not been received")
    elif color_image2.shape != (480, 640, 3):
        raise Exception("The last color image has not been received")
    elif depth_image2.shape != (480, 640):
        raise Exception("The last depth image has not been received")
    elif len(treatment_points) == 0:
        raise Exception("The treatment's points has not been received")

    ####################### TRABAJO DEL WORKER ##################
    p_trat = []
    for i in range(len(treatment_points)):
        p_trat.append([treatment_points[i]['x'], treatment_points[i]['y'],
                       treatment_points[i]['z']])  # - treatment_points[i]['height']/100])

    p_trat = np.asarray(p_trat)
    p_trat = np.append(p_trat, np.ones((len(p_trat), 1)), axis=1)

    """Matriz de transformacion homogenea para el paso de las coordenadas del robot a las coordenadas de la camara"""
    T = np.matrix([[0.9989, -0.0043, -0.0464, 0.5639],
                   [-0.0035, -0.9999, 0.0162, 0.1294],
                   [-0.0465, -0.0161, -0.9988, 0.6385],
                   [0, 0, 0, 1.0000]])  # cam_T_r Camara perpendicular al robot

    # Se transforman los puntos del tratamiento al sistema de coordenadas de la camara
    p_trat_t = T * p_trat.T
    p_trat_t = np.asarray(p_trat_t)[:3].T

    #if offset_active:
    """Metodos de calculo de offset: """
    # Se llama al primer metodo

    status1 = False

    try:
        status2, offset_pcd1 = pcpo.calcular_offset(color_image1, depth_image1, color_image2, depth_image2,
                                                    intrinsics1, intrinsics2, depth_scale1, depth_scale2,
                                                    p_trat_t)
    except Exception as e:
        raise Exception('status2: ' + str(e))

    # Se llama al tercer metodo
    # Este metodo alinea las dos point clouds con RANSAC
    try:
        status3, offset_pcd2 = pcpo2.calcular_offset(color_image1, depth_image1, color_image2, depth_image2,
                                                     intrinsics1, intrinsics2, depth_scale1, depth_scale2,
                                                     p_trat_t)
    except Exception as e:
        raise Exception('status3: ' + str(e))

    if status3:
        offset_media2 = offset_pcd2
        offset_media2 = (offset_media2 + offset_pcd2) / 2

        # offset_pcd1 = offset_media1
        offset_pcd2 = offset_media2

    # Comprobando resultados y se transforma el offset al marco del robot
    """El offset calculado esta en las coordenadas de la camara, se pasan a las coordenadas del robot"""
    offset_image_t = np.zeros(shape=(len(p_trat), 3))
    offset_pcd_t1 = np.zeros(shape=(len(p_trat), 3))
    offset_pcd_t2 = np.zeros(shape=(len(p_trat), 3))

    if status2:
        if (not offset_pcd1.shape == (len(p_trat), 3)):
            status2 = False
        elif not areTheyParallel(offset_pcd1, len(p_trat)):
            status2 = False
        else:
            offset_pcd1 = np.append(offset_pcd1, np.ones((len(offset_pcd1), 1)),
                                    axis=1)  # Se añade un 1 al final de cada vector para poder hacer la trnasformacion homogenea
            offset_pcd_t1 = T.T * offset_pcd1.T  # Se devuelve el offset a las coordenadas del robot
            offset_pcd_t1 = np.asarray(offset_pcd_t1)[:3].T
            # offset_pcd_t1 = np.around(offset_pcd_t1, decimals = 3) # Coordenadas del robot
            mod_off_pcd1 = np.linalg.norm(offset_pcd_t1, axis=1)
            mod_axis_off_pcd1 = np.mean(offset_pcd_t1, axis=1)
            # print("El desplazamiento con el metodo COVARIANCE: ", mod_off_pcd1)
            error_max = 0.5  # Desplazamiento maximo permitido en metros
            for i in range(len(mod_off_pcd1)):
                if mod_off_pcd1[i] > error_max:
                    status2 = False
            theta2 = np.arctan2(offset_pcd_t1[:, 2], offset_pcd_t1[:, 0])
            alpha2 = np.arctan2(offset_pcd_t1[:, 1], offset_pcd_t1[:, 0])

    if status3:
        if (not offset_pcd2.shape == (len(p_trat), 3)):
            status3 = False
        else:
            offset_pcd2 = np.append(offset_pcd2, np.ones((len(offset_pcd2), 1)),
                                    axis=1)  # Se añade un 1 al final de cada vector para poder hacer la trnasformacion homogenea
            offset_pcd_t2 = T.T * offset_pcd2.T  # Se devuelve el offset a las coordenadas del robot
            offset_pcd_t2 = np.asarray(offset_pcd_t2)[:3].T

            mod_off_pcd2 = np.linalg.norm(offset_pcd_t2, axis=1)
            error_max = 0.5  # Desplazamiento maximo permitido en metros
            for i in range(len(mod_off_pcd2)):
                if mod_off_pcd2[i] > error_max:
                    status3 = False

            mod_axis_off_pcd2 = np.mean(offset_pcd_t2, axis=1)
            # print("El desplazamiento con el metodo ICP: ", mod_off_pcd2)
            theta3 = np.arctan2(offset_pcd_t2[:, 2], offset_pcd_t2[:, 0])
            alpha3 = np.arctan2(offset_pcd_t2[:, 1], offset_pcd_t2[:, 0])
            print("Offset Metodos 3: ")
            print(status3)
            print(offset_pcd_t2)

    if status2 and status3:
        dif_giro_z = np.sqrt((alpha3 - alpha2) ** 2)
        print("Diferencia de giro en el eje z: ", dif_giro_z)
        error_max = 0.15  # error maximo permitido en radianes entre los dos metodos (radianes)
        for i in range(len(dif_giro_z)):
            if (dif_giro_z[i] > error_max) and (mod_axis_off_pcd2[i] > 0.01) and (mod_axis_off_pcd1[i] > 0.01):
                status2 = False

    """Deteccion errores:"""
    offset_mean = np.zeros((len(p_trat_t), 3), dtype=np.float32)
    array_status = np.array([status1, status2, status3])
    array_offsets = np.array([offset_image_t, offset_pcd_t1, offset_pcd_t2])
    error = False
    if (array_status == [False, False, False]).all():  # Fallan todos los metodos
        error = True
        print("Fallan todos los metodos.")
    elif (array_status == [False, False, True]).all():  # Fallan todos los metodos menos RANSAC
        # error = True
        print("Fallan todos los metodos menos RANSAC.")
        print("Se devuelve el offset aproximado")
    elif (array_status == [False, True, False]).all():  # Fallan todos los metodos menos COV
        error = True
        print("Fallan todos los metodos menos COVARIANCE point cloud.")
    elif (array_status == [False, True, True]).all():  # Falla el metodo ELLIPSIS
        print("Fallan el metodo ELLIPSIS.")
    elif (array_status == [True, False, False]).all():  # Fallan todos los metodos menos ELLIPSIS
        error = True
        print("Fallan todos los metodos menos ELLIPSIS.")
    elif (array_status == [True, False, True]).all():
        print("Falla el meotodo COVARIANCE.")
    elif (array_status == [True, True, False]).all():
        error = True
        print("Fallan el metodo RANSAC.")

    elif (array_status == [True, True, True]).all():
        # if mod_axis_off_pcd2[1]
        print("Todos los metodos han tenido exito. ")

    else:
        error = True

    """Con los resultados del offset calculado con los tres metodos se hace la media ponderada:"""
    if error == False:
        for p in range(len(p_trat_t)):
            for i in range(3):

                if i == 0:  # En el eje x (del robot)
                    array_pesos = np.array([0, 0.5, 0.5])[array_status]
                elif i == 2:  # En el eje z el metodo ELLIPSIS no aporta
                    array_pesos = np.array([0, 0.5, 0.5])[array_status]
                elif i == 1:  # En el eje y aportan los dos metodos
                    array_pesos = np.array([0.0, 0.2, 0.8])[array_status]

                offset_mean[p, i] = np.average(array_offsets[array_status, p, i], weights=array_pesos, axis=0)

        offset_final = offset_mean

        activate_vertical_offset = True

        offset_final = np.around(offset_final, decimals=4)  # Se redondea

        """Se comprueba que los puntos sean accesibles para el robot"""
        ptos_validos = validate_points(p_trat[:, :3], offset_final)
        if not ptos_validos:
            raise Exception('Points out of range')

        print(offset_final.tolist())
        return offset_final.tolist()
    else:
        raise Exception('Fail at the end')
    #for e in resultado:
    #    e[0], e[1] = -e[1], -e[0]
    #return resultado

