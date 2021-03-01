

  // --- Sin parámetros toma EV=0, prácticamente para pruebas
  Medicion::Medicion() {


    #ifdef EXP_DEBUG
        DEBUG_LIN( F("Constructor Medición sin parámetros") );
    #endif

    _init(K_EV0, K_EV0, K_EV0);

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Tenemos en la medición un EV total de ") );
    #endif

        DEBUG_TEX( _miEV );
        DEBUG_LIN();
  }

  // --- Constructor habitual, EV's para cada cada elemento fotométrico
  Medicion::Medicion(float f_EVini, float TV_EVini, float ISO_EVini) {

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Constructor Medición para, EV de f/=") );
        DEBUG_TEX( f_EVini );
        DEBUG_TEX( F(", EV de T/V=") );
        DEBUG_TEX( TV_EVini );
        DEBUG_TEX( F(", EV de ISO=") );
        DEBUG_TEX( ISO_EVini );
        DEBUG_LIN();
    #endif

    _init(f_EVini, TV_EVini, ISO_EVini);

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Tenemos en la medición un EV total de ") );
        DEBUG_TEX( _miEV );
        DEBUG_TEX( F(" EV's --- f/ ") );
        DEBUG_TEX( f::getTextoDecorado() );
        DEBUG_TEX( F(" --- T/V ") );
        DEBUG_TEX( TV::getTextoDecorado() );
        DEBUG_TEX( F(" --- ISO ") );
        DEBUG_TEX( ISO::getTextoDecorado() );
        DEBUG_LIN();
    #endif

  }

  // --- Constructor por TERCIOS para cada cada elemento fotométrico
  Medicion::Medicion(byte f_TERCIOini, byte TV_TERCIOini, byte ISO_TERCIOini) {

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Constructor Medición para, TERCIOS de f/=") );
        DEBUG_TEX( f_TERCIOini );
        DEBUG_TEX( F(", TERCIOS de T/V=") );
        DEBUG_TEX( TV_TERCIOini );
        DEBUG_TEX( F(", TERCIO de ISO=") );
        DEBUG_TEX( ISO_TERCIOini );
        DEBUG_LIN();
    #endif

    /*--Este constructor es especial, debe llamar a otros constructores, por eso
        no puede utilizar _init
    */
   f( (byte)f_TERCIOini );
   TV( (byte)TV_TERCIOini );
   ISO( (byte)ISO_TERCIOini );

    /*--Cada una de las invocaciones anteriores ha corregido si los EV's
        anteriores eran posibles, así que no hay que hacer verificación de
        errores.
    */
   _miEV = sumEVs();

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Tenemos en la medición un EV total de ") );
        DEBUG_TEX( _miEV );
        DEBUG_TEX( F(" EV's --- f/ ") );
        DEBUG_TEX( f::getTextoDecorado() );
        DEBUG_TEX( F(" --- T/V ") );
        DEBUG_TEX( TV::getTextoDecorado() );
        DEBUG_TEX( F(" --- ISO ") );
        DEBUG_TEX( ISO::getTextoDecorado() );
        DEBUG_LIN();
    #endif

  }



  /* --------------------------------------------------------------------------
        Métodos públicos
     --------------------------------------------------------------------------
  */

  // --- Generales


  // --- Obtener el EV de la medición
  float Medicion::getEV() { return _miEV; }


  // --- Establecer EN FIRME el EV de la medición
  void Medicion::setEV(float EV) {

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Acabo de recibir la orden de establecer EN FIRME un EV=") );
        DEBUG_TEX( EV );
        DEBUG_TEX( F(", Como yo tenía un EV" ) );
        DEBUG_TEX( _miEV );
        DEBUG_TEX( F("; me voy a acomodarlo") );
        DEBUG_LIN();
    #endif

    _enFirme = true;
    _miEV = EV;
    _acomodar();

  }

  // --- Sumar los EV's de las razones fotométricas implicadas
  float Medicion::sumEVs() {
       float _sumEV = f::getEV() + TV::getEV() + ISO::getEV();
       
       // --- Minimizar la imprecisión matemática de Arduino
       _sumEV = redondear(_sumEV, 4);

       return _sumEV;
  }





  // --- Perder un TERCIO de luz el f/
  bool Medicion::close_f() { return close_f(1); }
  
  // --- Perder varios TERCIOS de luz el f/
  bool Medicion::close_f(int TERCIOS) { return open_f( -TERCIOS ); }
  // ---                                            OJO: EN NEGATIVO

  // --- Ganar un TERCIO de luz el f/
  bool Medicion::open_f() { return open_f(+1); }

  // --- Ganar varios TERCIOS de luz el f/
  bool Medicion::open_f(int TERCIOS) {
    f::openTERCIOS(TERCIOS);
    return _acomodar();
  }

  // --- Perder un TERCIO de luz en el T/V
  bool Medicion::close_TV() { return close_TV(1); }

  // --- Perder varios TERCIOS de luz en T/V
  bool Medicion::close_TV(int TERCIOS) { return open_TV( -TERCIOS ); }
  // ---                                            OJO: EN NEGATIVO

  // --- Ganar un TERCIO de luz en el T/V
  bool Medicion::open_TV() { return open_TV(+1); }

  // --- Ganar varios TERCIOS de luz en T/V
  bool Medicion::open_TV(int TERCIOS) { return TV::openTERCIOS(TERCIOS); }




  // --- Para el ISO
  
  // --- Perder un TERCIO de luz en el ISO
  bool Medicion::close_ISO() { return close_ISO(1); }
  
  // --- Perder varios TERCIOS en el ISO
  bool Medicion::close_ISO(int TERCIOS) { return open_ISO( - TERCIOS ); }
   // ---                                            OJO: EN NEGATIVO
  
  // --- Ganar un TERCIO de luz en el ISO
  bool Medicion::open_ISO() { return open_ISO(+1); }
  
  // --- Ganar varios TERCIOS en el ISO
  bool Medicion::open_ISO(int TERCIOS) { return ISO::openTERCIOS(TERCIOS); }




  /* --------------------------------------------------------------------------
        Métodos privados
     --------------------------------------------------------------------------
  */

  // --- Acomodar el EV
  bool Medicion::_acomodar() {

    bool respFinal = true;

    #ifdef EXP_DEBUG
        DEBUG_TEX( F("Estoy acomodando, veamos si estoy EN FIRME ") );
        DEBUG_TEX( _enFirme );
        DEBUG_LIN();
    #endif

    // --- Cuando la medición está en firme, no podemos perder los EV's
    if (_enFirme) {

        /*--Ver cuanto suman los tres factores fotométricos. En caso de haber
            solicitado un cambio de un tercio en cualquier valor fotométrico,
            se reacomodará el valor liberado según la variable '_libre'. Cada
            factor fotométrico ha controlado por sí mismo si la orden recibida
            es posible y está dentro de sus límites, así que no debemos
            controlarlos, sólo sumar lo que sí tienen controlado y compensar
            con el elemento '_libre'
        */
        float _sumEV = sumEVs();

        // --- Sólo controlamos cuando hayan diferencias
        if (_miEV != _sumEV) {
            // --- Esta solución me da negativos o positivos según necesite
            float _dif = _miEV - _sumEV;

            // --- Convertimos a tercios, fin a la imprecisión de Arduino
            int _terciosDiferencia = EV_ABS().convertirEVaTERCIOS(_dif);


            #ifdef EXP_DEBUG
                DEBUG_TEX( F("Estoy acomodando, yo debo tener ") );
                DEBUG_TEX( _miEV );
                DEBUG_TEX( F(" y las razones fotométricas tienen ") );
                DEBUG_TEX( _sumEV );
                DEBUG_TEX( F(", encuentro una diferencia de ") );
                DEBUG_TEX( _dif );
                DEBUG_TEX( F(", debo acomodar ") );
                DEBUG_TEX( _terciosDiferencia );
                DEBUG_TEX( F(" TERCIOS") );
                DEBUG_LIN();
            #endif


            // --- Analicemos quién está libre
            bool _resp = true;

            switch (_libre) {
              case EL_f:
                #ifdef EXP_DEBUG
                    DEBUG_LIN( F("El f/ está libre") );
                #endif

                // --- Por esto responde false o true pero no se mira antes
                _resp = f::openTERCIOS(_terciosDiferencia);
                break;

              case EL_TV:
                #ifdef EXP_DEBUG
                    DEBUG_LIN( F("El T/V está libre") );
                #endif

                // --- Por esto responde false o true pero no se mira antes
                _resp = TV::openTERCIOS(_terciosDiferencia);
                break;

              case EL_ISO:
                #ifdef EXP_DEBUG
                    DEBUG_LIN( F("El ISO está libre") );
                #endif

                // --- Por esto responde false o true pero no se mira antes
                _resp = ISO::openTERCIOS(_terciosDiferencia);
                break;

              case TODOS:
                // --- Caso del super usiario, sin resolver
                break;
            }

            #ifdef EXP_DEBUG
                DEBUG_TEX( F("La respuesta del liberado es ") );
                DEBUG_TEX( _resp );
                DEBUG_LIN();
            #endif

            // --- Veamos que hacer si algún factor no pudo compensar
            if ( !_resp ) {
                _enFalso = true;
                respFinal = false;
            }
        }

    }

    return respFinal;
    // --- Si la medición no está en firme, no hay nada que acomodar

  }

}   // --- Espacio de nombres propio

#endif
