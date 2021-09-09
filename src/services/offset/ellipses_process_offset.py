import cv2
import numpy as np
from random import randrange 
import copy


"""Devuelve un vector en 3D en el marco de referencia de la camara a partir de
   un vector en 2D en el marge de referencia de la imagen y su profundidad."""
def Map_2D_To_3D(intrinsics, vector2D, depth):
    x = (vector2D[0]-intrinsics.ppx)/intrinsics.fx
    y = (vector2D[1]-intrinsics.ppy)/intrinsics.fy    
    
    return [int(depth*x), int(depth*y), int(depth)]

def Map_3D_To_2D(intrinsics, vector3D):
    x = -vector3D[0]/vector3D[2]
    y = vector3D[1]/vector3D[2]
   
    pixelX = int(np.floor(x * intrinsics.fx + intrinsics.ppx))
    pixelY = int(np.floor(y * intrinsics.fy + intrinsics.ppy))

    return [pixelX, pixelY]

def puntos_plano(mascara_color, depth_image):
    puntos=np.zeros((3,3),dtype=np.int32)
    i=0
    n=0
    while(i<3):
        if i==0:
            x = randrange(130,230)
            y = randrange(10,160)
            if mascara_color[y,x]==255 and mascara_color[y+2,x+2]==255 and mascara_color[y-2,x-2]==255:
                z=depth_image[y,x]
                puntos[i]=[y,x,z]
                i=i+1
        if i==1:
            x = randrange(380,500)
            y = randrange(10,160)
            if mascara_color[y,x]==255 and mascara_color[y+2,x+2]==255 and mascara_color[y-2,x-2]==255:
                z=depth_image[y,x]
                puntos[i]=[y,x,z]
                i=i+1
        if i==2:
            x = randrange(100,500)
            y = randrange(280,470)
            if mascara_color[y,x]==255 and mascara_color[y+2,x+2]==255 and mascara_color[y-2,x-2]==255:
                z=depth_image[y,x]
                puntos[i]=[y,x,z]
                i=i+1
        n=n+1
        if n>300:
            #print("No se encuentran puntos que correspondan con el color de la camilla", i)
            
            break
    return puntos

def ajustar_plano_por_3_puntos(puntos):
    #global vertices
    #v = np.int32(vertices)
    x1 = puntos[0,0]
    y1 = puntos[0,1]
    z1 = puntos[0,2]
    
    x2 =  puntos[1,0]
    y2 =  puntos[1,1]
    z2 =  puntos[1,2]
    
    x3 =  puntos[2,0]
    y3 =  puntos[2,1]
    z3 =  puntos[2,2]
    
    A = x2-x1
    B = y2-y1
    C = z2-z1
    D = x3-x1
    E = y3-y1
    F = z3-z1
    
    a = np.int64(B*F-C*E)
    b = np.int64(C*D-A*F)
    c = np.int64(A*E-B*D)
    
    d = np.int64(-(x1*a + y1*b + z1*c))  
    parameters_i = [-d/c, -a/c, -b/c]
    
    return parameters_i

def calcular_distancias_al_plano(h, w, parameters, offset_z):
    plano = np.empty((h, w), dtype=np.float32)
    for i in range(w):
        for j in range(h):
            plano[j,i] = j*parameters[1] + i*parameters[2] + parameters[0] + offset_z
    return plano

"""Borra todo lo que esté mas lejos que el plano indicado.
   Los vertices se detectan a partir de los puntos detectados como color de camilla o distancia al paciente
   Además borra la camilla a partir de lo que es su color"""
def borrar_fondo(depth_image, color_image, mascara_color,metodo,distancia_paciente=0):
    if (metodo==False):
        umbral=50
        puntos = puntos_plano(mascara_color,depth_image)
        parameters = ajustar_plano_por_3_puntos(puntos)
        h, w = depth_image.shape   
        plano = calcular_distancias_al_plano(h, w, parameters, 0)
    else:
        plano=distancia_paciente
        umbral=-150
    negro = 0
    blanco=255
    bg_removed_image=cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
    #donde la distancia es mayor que el plano de la camilla se pone en negro, el resto se deja en blanco
    bg_removed_image = np.where((depth_image > plano-umbral) | (depth_image <= 0), negro, bg_removed_image)
    bg_removed_image = np.where((depth_image <= plano-umbral), blanco, bg_removed_image)
    
    #donde la mascara de color detecta el color de la camilla se pone en negro
    bg_removed_image = np.where((mascara_color ==255), negro, bg_removed_image)

    bg_removed_image=borrar_bordes(bg_removed_image)
    #Se trata para borrar huecos y manchas
    bg_removed_image=tratar_imagen(bg_removed_image)
    return bg_removed_image

def obtener_vertices_elipse(angle, ma, MA, cx, cy):
    ang = angle+90;
    length = ma/2;
    x1 =  int(np.floor(cx - length * np.cos(ang * np.pi / 180.0)))
    y1 =  int(np.floor(cy - length * np.sin(ang * np.pi / 180.0)))
    x2 =  int(np.floor(cx + length * np.cos(ang * np.pi / 180.0)))
    y2 =  int(np.floor(cy + length * np.sin(ang * np.pi / 180.0)))      
    ang = angle;
    length = MA/2; 
    x3 =  int(np.floor(cx - length * np.cos(ang * np.pi / 180.0)))
    y3 =  int(np.floor(cy - length * np.sin(ang * np.pi / 180.0)))
    x4 =  int(np.floor(cx + length * np.cos(ang * np.pi / 180.0)))
    y4 =  int(np.floor(cy + length * np.sin(ang * np.pi / 180.0)))      
    
    return x1,y1,x2,y2,x3,y3,x4,y4

def buscar_camilla(color_image):
    image_hsv = cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    azul_bajos = np.array([90,125,0])
    azul_altos = np.array([110,255,255])
    mascara_color = cv2.inRange(image_hsv, azul_bajos, azul_altos)
    mascara_color=tratar_imagen(mascara_color)

    return mascara_color

def buscar_piel(color_image):
    image_hsv = cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    #detección de piel
    lower = np.array([0, 40, 80], dtype = "uint8")
    upper = np.array([40, 255, 255], dtype = "uint8")
    color_image = cv2.GaussianBlur(color_image, (5,5), 3)
    mascara_piel = cv2.inRange(image_hsv, lower, upper)
    
    mascara_piel=borrar_bordes(mascara_piel)
    mascara_piel=tratar_imagen(mascara_piel)

    return mascara_piel

def invertir_colores(imagen):
    imagen2=imagen
    imagen2=np.where(imagen==255,0,imagen2)
    imagen2=np.where(imagen==0,255,imagen2)
    imagen=imagen2

    return imagen
   
def borrar_bordes(imagen):
   #print("Funcion borrar bordes: ")
   # print(imagen.shape)
    for y in range (640):
        for x in range (470,480):
            imagen[x,y]=0
        for x in range (0,10):
            imagen[x,y]=0
    for x in range(480):
        for y in range (560,640):
            imagen[x,y]=0
        for y in range (0,80):
            imagen[x,y]=0

    imagen=tratar_imagen(imagen)

    return imagen
    
def elipses(contorno,color_image):
    (cx,cy),(MA,ma),angle = cv2.fitEllipse(contorno)
    cv2.ellipse(color_image, ((cx,cy),(MA,ma),angle),(0,0,255),2)
    x1,y1,x2,y2,x3,y3,x4,y4 = obtener_vertices_elipse(angle, ma, MA, cx, cy)
    cv2.line(color_image,(x1,y1),(x2,y2),(255,0,0),2)
    cv2.line(color_image,(x3,y3),(x4,y4),(255,0,0),2)
    return cx,cy,angle

def metodo_elipse(puntos_tratamiento,imagen1,imagen2,contorno1,contorno2,depth_image1,depth_image2,intrinsics1,intrinsics2,depth_scale1,depth_scale2):
    
    #Se dibujan los contornos
    cv2.drawContours(imagen1, [contorno1], 0, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.drawContours(imagen2, [contorno2], 0, (0, 255, 0), 2, cv2.LINE_AA)
    
    #Se dibujan las elipses sobre las imagenes y se reciben los parametros necesarios
    cx1,cy1,angle1=elipses(contorno1,imagen1)
    cx2,cy2,angle2=elipses(contorno2,imagen2)
    
    #Dibujo de los puntos de tratamiento sobre la primera imagen y se calcula su distancia con respecto al centro de la elipse
    puntos1=np.empty((len(puntos_tratamiento),2))
    offset1=np.empty((len(puntos_tratamiento),2))
    for i in range(len(puntos_tratamiento)):
        puntos1[i]= Map_3D_To_2D(intrinsics1,puntos_tratamiento[i])
        cv2.circle(imagen1, (int(puntos1[i,0]),int(puntos1[i,1])), 5, (0, 0, 255), -1)
        offset1[i,0]=np.floor(cx1-puntos1[i,0])
        offset1[i,1]=np.floor(cy1-puntos1[i,1])
       
    if abs(angle1) > 50:
        angle1 = (angle1-180)
    if abs(angle2) > 50:
        angle2 = (angle2-180)
        
    angulo = angle1 - angle2
    
    print("Angulo: " + str(angulo))
    #Se giran los puntos de la primera imagen el ángulo calculado y se situan en la segunda imagen
    mat = np.matrix([[np.cos(np.deg2rad(angulo)), -np.sin(np.deg2rad(angulo))], [np.sin(np.deg2rad(angulo)), np.cos(np.deg2rad(angulo))]])
    offset2=np.empty((len(puntos_tratamiento),2))
    offset2=offset1*mat
    puntos2=np.empty((len(puntos_tratamiento),2))   
    for i in range(len(puntos_tratamiento)):
        puntos2[i,0]=np.floor(cx2-offset2[i,0])
        puntos2[i,1]=np.floor(cy2-offset2[i,1])
        cv2.circle(imagen2, (int(puntos2[i,0]),int(puntos2[i,1])), 5, (0, 0, 255), -1)
    #Se calcula el desplazamiento entre los puntos de la primera imagen y los de la segunda
    offset=np.empty((len(puntos_tratamiento),3))
    vector3D_1=np.empty((len(puntos_tratamiento),3))
    vector3D_2=np.empty((len(puntos_tratamiento),3))
    
    for i in range(len(puntos_tratamiento)):
        vector3D_1[i]=Map_2D_To_3D(intrinsics1,[int(puntos1[i,0]),int(puntos1[i,1])],puntos_tratamiento[i,2]/depth_scale1)
        vector3D_2[i]=Map_2D_To_3D(intrinsics2,[int(puntos2[i,0]),int(puntos2[i,1])],puntos_tratamiento[i,2]/depth_scale2)

        offset[i,0]=round(depth_scale1*(vector3D_2[i,0]-vector3D_1[i,0]),3)
        offset[i,1]=round(depth_scale1*(vector3D_2[i,1]-vector3D_1[i,1]),3)
        offset[i,2]=round(depth_scale1*(vector3D_2[i,2]-vector3D_1[i,2]),3)
            
    return offset,imagen1,imagen2


def buscar_contorno(imagen):
    _, contours, _ = cv2.findContours(imagen,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    if len(contours) < 1:
        return 0, False
    cntsSorted=sorted(contours, key=cv2.contourArea, reverse=True)
    contorno = cntsSorted[0]
    if cv2.contourArea(contorno) <8000 or cv2.contourArea(contorno) >150000:
        return 0,False
    return contorno, True

def graficar(imagen1,imagen2,similaridad,offset, n_metodo):
    print("Similaridad metodo_"+str(n_metodo)+": " +str(similaridad))
    print('offset:',offset)
    windowname = "Metodo"+str(n_metodo)
    img_juntas = np.hstack((imagen1, imagen2))              
    cv2.imshow(windowname, img_juntas) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return  

def tratar_imagen(imagen):
    kernel = np.ones((5,5),np.uint8)
    imagen = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
    imagen = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)
    return imagen

def desplazamiento_espalda_metodo1(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision):
    imagen1=copy.deepcopy(color_image1)
    imagen2=copy.deepcopy(color_image2)
    #Se busca el color de la camilla y se adapta para buscar el contorno del cuerpo
    mascara_color1=buscar_camilla(imagen1)
    mascara_color2=buscar_camilla(imagen2)
    mascara_color1=invertir_colores(mascara_color1)  
    mascara_color2=invertir_colores(mascara_color2)
    mascara_color1=borrar_bordes(mascara_color1)  
    mascara_color2=borrar_bordes(mascara_color2)
    """
    windowname = "Mascara color metodo1"
    img_juntas = np.hstack((mascara_color1, mascara_color2))              
    cv2.imshow(windowname, img_juntas) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    #Se buscan los contornos sobre las imagenes binarizadas
    contorno1,valido1=buscar_contorno(mascara_color1)
    contorno2,valido2=buscar_contorno(mascara_color2)
    if valido1==False or valido2==False:
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset     
    #Se evalúa la calidad de los contornos
    similaridad = cv2.matchShapes(contorno1,contorno2,1,0.0)
    if similaridad >precision:
        #print(similaridad)
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset
    
    
    #Se llama a la función que a partir de los datos obtenidos nos devuelve el offset, también devuelve las imagenes con los puntos de definición
    #de tratamiento y de aplicación de tratamiento, para visualizar a modo de comprobación
    
    estado=True
    offset, imagen1, imagen2=metodo_elipse(puntos_tratamiento,imagen1,imagen2,contorno1,contorno2,depth_image1,depth_image2,intrinsics1,intrinsics2,depth_scale1,depth_scale2)
    
    #Se imprime el offset y se visualizan las imagenes a modo de comprobación
    if grafico:
        graficar(imagen1,imagen2,similaridad,offset,1)
    
    return  estado, offset

def desplazamiento_espalda_metodo2(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision):
    imagen1=copy.deepcopy(color_image1)
    imagen2=copy.deepcopy(color_image2)
    #Se busca el color de la camilla
    mascara_color1=buscar_camilla(imagen1)
    mascara_color2=buscar_camilla(imagen2)
    mascara_color1=borrar_bordes(mascara_color1)
    mascara_color2=borrar_bordes(mascara_color2)

    #Se les borra el fondo a las imagenes en color
    bg_removed_image1 = borrar_fondo(depth_image1, imagen1,mascara_color1,False)
    bg_removed_image2 = borrar_fondo(depth_image2, imagen2,mascara_color2,False)

    #Se buscan los contornos sobre las imagenes binarizadas
    contorno1,valido1 = buscar_contorno(bg_removed_image1)
    contorno2,valido2 = buscar_contorno(bg_removed_image2)
    
    if valido1==False or valido2==False:
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset 
    #Se evalúa la calidad de los contornos
    similaridad = cv2.matchShapes(contorno1,contorno2,1,0.0)
    n=0
    while(similaridad>precision):
        bg_removed_image1 = borrar_fondo(depth_image1, imagen1, mascara_color1,False) 
        bg_removed_image2 = borrar_fondo(depth_image2, imagen2, mascara_color2,False)
        contorno1, valido1 = buscar_contorno(bg_removed_image1)
        contorno2, valido2 = buscar_contorno(bg_removed_image2)
        if valido1 and valido2:
            similaridad = cv2.matchShapes(contorno1,contorno2,1,0.0)
        #print("Similaridad: " +str(similaridad))
        n=n+1
        if n==25:#50
            #print("Las imagenes son demasiado diferentes, el resultado puede no ser el esperado")
            estado=False
            offset=offset=np.empty((len(puntos_tratamiento),3))
            return estado, offset
    
    
    estado=True
    #Se llama a la función que a partir de los datos obtenidos nos devuelve el offset, también devuelve las imagenes con los puntos de definición
    #de tratamiento y de aplicación de tratamiento, para visualizar a modo de comprobación
    offset, imagen1, imagen2=metodo_elipse(puntos_tratamiento,imagen1,imagen2,contorno1,contorno2,depth_image1,depth_image2,intrinsics1,intrinsics2,depth_scale1,depth_scale2)
    
    #Se imprime el offset y se visualizan las imagenes a modo de comprobación
    if grafico:
        graficar(imagen1,imagen2,similaridad,offset,2)
        
    return  estado, offset

"""Los frames de color y profundidad deben llegar ya alineados"""
def desplazamiento_espalda_metodo3(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision):
    imagen1=copy.deepcopy(color_image1)
    imagen2=copy.deepcopy(color_image2)
    #Se busca el color de la piel y se adapta para buscar el contorno del cuerpo
    mascara_color1=buscar_piel(imagen1)
    mascara_color2=buscar_piel(imagen2)
    
    #Se buscan los contornos sobre las imagenes binarizadas
    contorno1,valido1=buscar_contorno(mascara_color1)
    contorno2,valido2=buscar_contorno(mascara_color2)
    if valido1==False or valido2==False:
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset
    #Se evalúa la calidad de los contornos
    similaridad = cv2.matchShapes(contorno1,contorno2,1,0.0)
    if similaridad >precision:
        #print(similaridad)
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset
    

    
    estado=True
    #Se llama a la función que a partir de los datos obtenidos nos devuelve el offset, también devuelve las imagenes con los puntos de definición
    #de tratamiento y de aplicación de tratamiento, para visualizar a modo de comprobación
    offset, imagen1, imagen2=metodo_elipse(puntos_tratamiento,imagen1,imagen2,contorno1,contorno2,depth_image1,depth_image2,intrinsics1,intrinsics2,depth_scale1,depth_scale2)
    
    #Se imprime el offset y se visualizan las imagenes a modo de comprobación
    if grafico:
        graficar(imagen1,imagen2,similaridad,offset,3)
    return  estado, offset
def desplazamiento_espalda_metodo4(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision):
    imagen1=copy.deepcopy(color_image1)
    imagen2=copy.deepcopy(color_image2)
    #Se les borra el fondo a las imagenes en color 
    #distancia_paciente=abs(min(puntos_tratamiento[:,2])*1000)
    distancia_paciente=650
    #print(distancia_paciente)
    metodo=True
    bg_removed_image1 = borrar_fondo(depth_image1, imagen1,0,metodo,distancia_paciente)
    bg_removed_image2 = borrar_fondo(depth_image2, imagen2,0,metodo,distancia_paciente)

    #Se buscan los contornos sobre las imagenes binarizadas
    contorno1,valido1=buscar_contorno(bg_removed_image1)
    contorno2,valido2=buscar_contorno(bg_removed_image2)
    if valido1==False or valido2==False:
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset 
    #Se evalúa la calidad de los contornos
    similaridad = cv2.matchShapes(contorno1,contorno2,1,0.0)
    if similaridad >precision:
        #print(similaridad)
        estado=False
        offset=offset=np.empty((len(puntos_tratamiento),3))
        return estado, offset
    
    estado= True
    #Se llama a la función que a partir de los datos obtenidos nos devuelve el offset, también devuelve las imagenes con los puntos de definición
    #de tratamiento y de aplicación de tratamiento, para visualizar a modo de comprobación
    offset, imagen1, imagen2=metodo_elipse(puntos_tratamiento,imagen1,imagen2,contorno1,contorno2,depth_image1,depth_image2,intrinsics1,intrinsics2,depth_scale1,depth_scale2)
    
    #Se imprime el offset y se visualizan las imagenes a modo de comprobación
    if grafico:
        graficar(imagen1,imagen2,similaridad,offset,4)
    
    return  estado, offset


def desplazamiento_espalda_contornos(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision=0.05):
    #estado1, offset1 = desplazamiento_espalda_metodo1(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision)
    #estado2, offset2 = desplazamiento_espalda_metodo2(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision)
    #estado3, offset3 = desplazamiento_espalda_metodo3(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision)
    estado4, offset4 = desplazamiento_espalda_metodo4(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision)
        
    offset=np.zeros((len(puntos_tratamiento),3),dtype=np.float32)
    
    estado1 = False
    estado2 = False
    estado3 = False
    """
    array_offsets = np.array([offset1, offset2, offset3, offset4])
    array_status =  np.array([estado1, estado2, estado3, estado4])
    
    for p in range(len(puntos_tratamiento)):
        for i in range(2):
            offset[p,i] = np.mean(array_offsets[array_status == True,p,i])
            if array_status[i]:
                estado=True
    """           
    
    if offset.shape == (len(puntos_tratamiento),3): 
        offset = offset4
        estado = True
    else:
        estado = False
        
    return estado, offset
#estado, offset = desplazamiento_espalda_contornos(color_image1, depth_image1, color_image2, depth_image2, intrinsics1, intrinsics2,depth_scale1, depth_scale2, puntos_tratamiento,grafico,precision)