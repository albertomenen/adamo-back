from ...utils.s3 import get_from_aws
from ...utils.schemas.treatment import treatment_offset


def from_model_to_offset(old_treatment, new_treatment):
    firstImage = treatment_offset.dump(old_treatment)
    try:
        firstImage['image_3D_depth'] = get_from_aws(firstImage['image_3D_depth'], to_ascii=False)
        firstImage['image_3D_color'] = get_from_aws(firstImage['image_3D_color'], to_ascii=False)
    except:
        raise Exception('Cant find images')
    lastImage = treatment_offset.dump(new_treatment)
    response = {
        'firstImage': {
            "idColor": firstImage['image_3D_color'],
            "idDepth": firstImage['image_3D_depth'],
            "width": firstImage['width'],
            "height": firstImage['height'],
            "ppx": firstImage['ppx'],
            "ppy": firstImage['ppy'],
            "fx": firstImage['fx'],
            "fy": firstImage['fy'],
            "model": firstImage['model'],
            "coeff": firstImage['coeff'],
            "depthScale": firstImage['depth_scale']
        },
        'lastImage': {
            "idColor": lastImage['image_3D_color'].encode(),
            "idDepth": lastImage['image_3D_depth'].encode(),
            "width": lastImage['width'],
            "height": lastImage['height'],
            "ppx": lastImage['ppx'],
            "ppy": lastImage['ppy'],
            "fx": lastImage['fx'],
            "fy": lastImage['fy'],
            "model": lastImage['model'],
            "coeff": lastImage['coeff'],
            "depthScale": lastImage['depth_scale']
        },
        'points': firstImage['points']
    }
    return response
