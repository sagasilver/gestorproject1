
            function pregunta_cliente(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar este cliente?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }

             function pregunta_usuario(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar este usuario?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }
             function pregunta_rol(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar este rol?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }

            function pregunta_flujo(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar este flujo?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }
            function pregunta_hu(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar esta Historia de Usuario?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }
            function pregunta_miembro(){
                if ( ! confirm('¿Esta seguro/a que desea eliminar este miembro del equipo?')){
                        return false;
                }
                else
                {
                    return true;
                }

            }

function validar(){
var ok = 0;
var ckbox = document.getElementsByName('hu');
    for (var i=0; i < ckbox.length; i++){
        if(ckbox[i].checked == true){
        ok = 1;
        }
    }

    if(ok == 0){
    alert('indique al menos un HU');
    return false;
    }
}
