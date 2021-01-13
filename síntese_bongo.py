def bongo(f0):
  fs = 44100
  T0 = 1/f0
  N0 = int(T0 * fs)
  
  atraso = np.zeros(N0)
  # edicao do 1 e ultimo valor de atraso
  atraso[0] = 1
  atraso[-1] = -0.9; # aumenta a duracao
  b = [1] # valor maximo

  x = np.zeros(11025) # fs*1  tempo total
  x[0] = 1 # impulso

  #b=1 sem propagação atraso ao longo do tempo
  y = scipy.signal.lfilter( b, atraso, x)
  #y2 = scipy.signal.lfilter(-b, atraso, x)
  t = np.arange(len(y))/fs

  plt.figure()
  plt.plot(t,y)
  #plt.xlim([0,1])
  plt.show()

  # Aqui começa a apresentar som de bongo  
  b0, a0 = scipy.signal.iirpeak(f0, 50, fs=fs) #880
  y0 = scipy.signal.lfilter(b0,a0,y)
  Audio(data=y0, rate=fs)
  
  # filtros baixa/ 50 60
  x1 = scipy.signal.oaconvolve(y0, np.hanning(50))
  y1 = scipy.signal.lfilter(b, atraso, y0/2)
  Audio(data=y1, rate=fs)

  #criar um sinal aleatorio, raspando uma corda 100, 50, 20
  x22 = np.random.randn(int(fs/100))-120 #fs/10
  x22 = np.hstack( (x22, np.zeros(22050))) #11025
  y2 = scipy.signal.lfilter(b, atraso, x22)
  Audio(data=y2, rate=fs)

  # filtro passa bandas #retirar freq, 2db
  b0, a0 = scipy.signal.iirpeak( f0*2.042, Q = 40, fs=fs )
  y_02 = scipy.signal.lfilter(b0, a0, y2) #y2; y1
  rn = np.random.uniform(0.01,0.09, size=y_02.shape)
  rn = scipy.signal.oaconvolve(rn[:-69], np.hanning(70))
  y_03 = y_02+rn 

  #y_02 = y_01*2**(1/12)
  #convolucao com 
  #c_1 =c1/2
  #y_01 = scipy.signal.oaconvolve(c_1, y_01 )

  #Audio(data=y_03, rate=fs)

  return y_03
