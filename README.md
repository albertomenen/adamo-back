# adamo-back



## Getting started

Para arrancar es necesario tener docker instalado.

docker run --rm --name='mailcatcher' -d \
  --publish=1069:1080 \
  --publish=1029:1025 \
dockage/mailcatcher:0.6.5