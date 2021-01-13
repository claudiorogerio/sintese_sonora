def baixo(f0):  
  fs = 44100
  T0 = 1/f0
  N0 = int(T0 * fs)
  atraso = np.zeros(N0)
  # edicao do 1 e ultimo valor de atraso
  atraso[0] = 1
  atraso[-1] = -0.8; # aumenta a duracao
  b = [1] # valor maximo

  x = np.zeros(11025) # fs*1  tempo total
  x[0] = 1 # impulso

  #b=1 sem propagação atraso ao longo do tempo
  y = scipy.signal.lfilter( b, atraso, x)
  #y2 = scipy.signal.lfilter(-b, atraso, x)
  t = np.arange(len(y))/fs

  #plt.figure()
  #plt.plot(t,y)
  #plt.xlim([0,1])
  #plt.show()
    
  #criar um sinal aleatorio, raspando uma corda 100, 50, 20
  x22 = np.random.randn(int(fs/100))-120 #fs/10
  x22 = np.hstack( (x22, np.zeros(22050))) #11025
  yb2 = scipy.signal.lfilter(b, atraso, x22)
  #Audio(data=yb2, rate=fs)

  # filtro passa bandas #retirar freq, 2db
  b0, a0 = scipy.signal.iirpeak( f0/2, Q=50, fs=fs )
  yb02 = scipy.signal.lfilter(b0, a0, y2) #y2; y1

  Audio(data=yb02, rate=fs)

  # filtro passa bandas #retirar freq, 2db
  b0, a0 = scipy.signal.iirpeak( f0/4, Q=60, fs=fs )

  # notas as criar y_b01, y_b02, y_b03 ...
  y_b03 = scipy.signal.lfilter(b0, a0, yb2) #y2; y1

  #Audio(data=y_b03, rate=fs)

  return y_b03
