def gaita( f0 ):
  #f0 = 1008/2
  fs = 44100
  T0 = 1/f0
  N0 = int(T0 * fs)
  atraso = np.zeros(N0)
  # edicao do 1 e ultimo valor de atraso
  atraso[0] = 1
  atraso[-1] = -0.99; # aumenta a duracao
  b = [1] # valor maximo

  x = np.zeros(fs) # fs*1  tempo total
  x[0] = 1 # impulso

  #b=1 sem propagação atraso ao longo do tempo
  y = scipy.signal.lfilter( b, atraso, x)
  #y2 = scipy.signal.lfilter(-b, atraso, x)
  t = np.arange(len(y))/fs

  #plt.figure()
  #plt.plot(t,y)
  #plt.xlim([0,1])
  #plt.show()

  b0, a0 = scipy.signal.iirpeak(f0/4, 100, fs=fs) #880
  y0 = scipy.signal.lfilter(b0,a0,y)
  #Audio(data=y0, rate=fs)

  x1 = scipy.signal.oaconvolve(y0, np.hanning(40))
  y1 = scipy.signal.lfilter(b, atraso, y0)
  #Audio(data=y1, rate=fs)

  x22 = np.random.randn(int(fs))+10 #fs/10
  x22 = np.hstack( (x22, np.zeros(fs*2))) #11025
  y2 = scipy.signal.lfilter(b, atraso, y1) #x22
  #Audio(data=y2, rate=fs)

  b0, a0 = scipy.signal.iirpeak( f0*.09, 20, fs=fs )
  y_g01 = scipy.signal.lfilter(b0, a0, y2) #y2; y1

  return y_g01
