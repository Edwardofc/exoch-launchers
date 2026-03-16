'use client';

import React, { useState, useEffect } from 'react';

interface Account {
  id: string;
  name: string;
  type: 'microsoft' | 'crack' | 'local';
  skinUrl?: string;
}

interface Settings {
  ram: { min: number; max: number };
  javaPath: string;
  resolution: { width: number; height: number };
  fullscreen: boolean;
  maxFps: number;
  renderDistance: number;
}

interface Server {
  name: string;
  ip: string;
  players: string;
}

interface News {
  id: number;
  title: string;
  date: string;
  image: string;
}

export default function MinecraftLauncher() {
  const [activeTab, setActiveTab] = useState('play');
  const [accounts, setAccounts] = useState<Account[]>([
    { id: '1', name: 'Player', type: 'local', skinUrl: 'https://crafatar.com/avatars/7a0776e4465b45ca8a0a5d30d2955c70?size=128' },
    { id: '2', name: 'Gamer', type: 'microsoft' },
  ]);
  const [selectedAccount, setSelectedAccount] = useState<string>('1');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isAccountsOpen, setIsAccountsOpen] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [isLaunching, setIsLaunching] = useState(false);
  const [launchProgress, setLaunchProgress] = useState(0);
  const [launchStep, setLaunchStep] = useState('');
  
  const [settings, setSettings] = useState<Settings>({
    ram: { min: 2, max: 4 },
    javaPath: 'java',
    resolution: { width: 1920, height: 1080 },
    fullscreen: true,
    maxFps: 240,
    renderDistance: 12,
  });

  const servers: Server[] = [
    { name: 'Hypixel', ip: 'mc.hypixel.net', players: '65,234/100,000' },
    { name: 'Mineplex', ip: 'us.mineplex.com', players: '12,345/20,000' },
    { name: 'CubeCraft Games', ip: 'play.cubecraft.net', players: '8,765/15,000' },
  ];

  const news: News[] = [
    { 
      id: 1, 
      title: 'Minecraft 1.21 Update Released!', 
      date: '3 días atrás',
      image: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&h=400&fit=crop'
    },
    { 
      id: 2, 
      title: 'New Server Features', 
      date: '1 semana atrás',
      image: 'https://images.unsplash.com/photo-1614728853846-70e178874925?w=600&h=400&fit=crop'
    },
  ];

  useEffect(() => {
    console.log('Launcher inicializado');
  }, []);

  const handleLaunch = async () => {
    setIsLaunching(true);
    setLaunchProgress(0);
    setLaunchStep('Verificando archivos...');

    const steps = [
      { progress: 20, step: 'Descargando recursos...' },
      { progress: 45, step: 'Preparando entorno...' },
      { progress: 65, step: 'Iniciando Java...' },
      { progress: 85, step: 'Cargando juego...' },
      { progress: 100, step: 'Listo para jugar!' },
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLaunchProgress(steps[i].progress);
      setLaunchStep(steps[i].step);
    }

    await new Promise(resolve => setTimeout(resolve, 800));
    setIsLaunching(false);
    
    if (activeTab === 'play') {
      console.log('Juego iniciado con:');
      console.log('Cuenta:', selectedAccount);
      console.log('RAM:', `${settings.ram.min}GB - ${settings.ram.max}GB`);
      console.log('Resolución:', `${settings.resolution.width}x${settings.resolution.height}`);
    }
  };

  const handleRamChange = (type: 'min' | 'max', value: number) => {
    if (value <= 0) return;
    
    const newSettings = { ...settings };
    
    if (type === 'min') {
      if (value <= newSettings.ram.max) {
        newSettings.ram.min = value;
      }
    } else {
      if (value >= newSettings.ram.min) {
        newSettings.ram.max = value;
      }
    }
    
    setSettings(newSettings);
  };

  const handleResolutionChange = (width: number, height: number) => {
    setSettings({
      ...settings,
      resolution: { width, height },
    });
  };

  const handleAccountAdd = (name: string, type: 'microsoft' | 'crack' | 'local') => {
    const newAccount: Account = {
      id: Date.now().toString(),
      name,
      type,
    };
    setAccounts([...accounts, newAccount]);
    setSelectedAccount(newAccount.id);
  };

  const handleAccountRemove = (accountId: string) => {
    if (accounts.length <= 1) return;
    
    const filteredAccounts = accounts.filter(acc => acc.id !== accountId);
    setAccounts(filteredAccounts);
    
    if (selectedAccount === accountId) {
      setSelectedAccount(filteredAccounts[0].id);
    }
  };

  const getAccountTypeText = (type: 'microsoft' | 'crack' | 'local') => {
    switch (type) {
      case 'microsoft': return 'Microsoft';
      case 'crack': return 'Crack';
      case 'local': return 'Local';
    }
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-white font-sans selection:bg-blue-500/30 overflow-hidden">
      
      <header className="bg-black/30 backdrop-blur-md border-b border-neutral-700/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-600 rounded-lg flex items-center justify-center shadow-lg">
              <span className="text-lg font-bold">M</span>
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-green-500 to-blue-600 bg-clip-text text-transparent hidden md:block">
              LauncherPro
            </h1>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('play')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'play' 
                    ? 'bg-blue-600 text-white shadow-lg' 
                    : 'bg-neutral-800 text-neutral-400 hover:bg-neutral-700 hover:text-white'
                }`}
              >
                Play
              </button>
              <button
                onClick={() => setActiveTab('servers')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'servers' 
                    ? 'bg-blue-600 text-white shadow-lg' 
                    : 'bg-neutral-800 text-neutral-400 hover:bg-neutral-700 hover:text-white'
                }`}
              >
                Servidores
              </button>
              <button
                onClick={() => setActiveTab('news')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'news' 
                    ? 'bg-blue-600 text-white shadow-lg' 
                    : 'bg-neutral-800 text-neutral-400 hover:bg-neutral-700 hover:text-white'
                }`}
              >
                Noticias
              </button>
            </div>

            <div className="relative">
              <button
                onClick={() => setIsAccountsOpen(!isAccountsOpen)}
                className="flex items-center gap-3 px-4 py-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 transition-all border border-neutral-700/50"
              >
                <img 
                  src={accounts.find(a => a.id === selectedAccount)?.skinUrl || 'https://crafatar.com/avatars/7a0776e4465b45ca8a0a5d30d2955c70?size=32'}
                  alt="Account" 
                  className="w-8 h-8 rounded-full border-2 border-blue-500"
                />
                <span className="text-sm font-medium hidden sm:inline">
                  {accounts.find(a => a.id === selectedAccount)?.name || 'Player'}
                </span>
                <svg 
                  className={`w-4 h-4 text-neutral-400 transition-transform ${isAccountsOpen ? 'rotate-180' : ''}`} 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {isAccountsOpen && (
                <div className="absolute right-0 mt-2 w-80 bg-neutral-800 border border-neutral-700 rounded-lg shadow-xl py-2 z-50">
                  {accounts.map(account => (
                    <div 
                      key={account.id} 
                      className={`px-4 py-3 flex items-center gap-3 cursor-pointer transition-all hover:bg-neutral-700 ${
                        selectedAccount === account.id ? 'bg-neutral-700 border-l-4 border-blue-500' : ''
                      }`}
                      onClick={() => setSelectedAccount(account.id)}
                    >
                      <img 
                        src={account.skinUrl || 'https://crafatar.com/avatars/7a0776e4465b45ca8a0a5d30d2955c70?size=40'} 
                        alt={account.name} 
                        className="w-10 h-10 rounded-full"
                      />
                      <div className="flex-1">
                        <div className="font-medium text-sm">{account.name}</div>
                        <div className="text-xs text-neutral-400">{getAccountTypeText(account.type)}</div>
                      </div>
                      <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        {accounts.length > 1 && (
                          <button 
                            onClick={(e) => {
                              e.stopPropagation();
                              handleAccountRemove(account.id);
                            }}
                            className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  <hr className="border-neutral-700 my-2" />
                  
                  <button 
                    onClick={() => handleAccountAdd('NewPlayer', 'local')}
                    className="w-full px-4 py-3 flex items-center gap-3 text-blue-400 hover:bg-neutral-700 transition-all"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    <span className="text-sm font-medium">Añadir Cuenta</span>
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={() => setIsSettingsOpen(!isSettingsOpen)}
              className="p-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 transition-all border border-neutral-700/50"
              title="Ajustes"
            >
              <svg className="w-5 h-5 text-neutral-400 hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'play' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 shadow-xl">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold bg-gradient-to-r from-green-500 to-blue-600 bg-clip-text text-transparent">
                    Minecraft
                  </h2>
                  <div className="text-sm text-neutral-400">v1.21.1</div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-neutral-900 rounded-lg p-4 border border-neutral-700 hover:border-blue-500/50 transition-all">
                    <div className="text-xs text-neutral-400 mb-1">FPS Máx.</div>
                    <div className="font-mono text-lg">{settings.maxFps}</div>
                  </div>
                  <div className="bg-neutral-900 rounded-lg p-4 border border-neutral-700 hover:border-blue-500/50 transition-all">
                    <div className="text-xs text-neutral-400 mb-1">Distancia Render</div>
                    <div className="font-mono text-lg">{settings.renderDistance} Chunks</div>
                  </div>
                  <div className="bg-neutral-900 rounded-lg p-4 border border-neutral-700 hover:border-blue-500/50 transition-all">
                    <div className="text-xs text-neutral-400 mb-1">RAM Máx.</div>
                    <div className="font-mono text-lg">{settings.ram.max}GB</div>
                  </div>
                  <div className="bg-neutral-900 rounded-lg p-4 border border-neutral-700 hover:border-blue-500/50 transition-all">
                    <div className="text-xs text-neutral-400 mb-1">Resolución</div>
                    <div className="font-mono text-lg">{settings.resolution.width}x{settings.resolution.height}</div>
                  </div>
                </div>

                <button
                  onClick={handleLaunch}
                  disabled={isLaunching}
                  className={`w-full py-4 px-6 rounded-lg font-bold text-lg transition-all transform hover:scale-105 active:scale-95 ${
                    isLaunching
                      ? 'bg-neutral-700 cursor-not-allowed'
                      : 'bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 shadow-lg hover:shadow-2xl'
                  }`}
                >
                  {isLaunching ? 'Iniciando...' : 'Jugar'}
                </button>

                {isLaunching && (
                  <div className="mt-4">
                    <div className="h-2 bg-neutral-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-green-500 to-blue-600 transition-all duration-500"
                        style={{ width: `${launchProgress}%` }}
                      />
                    </div>
                    <div className="text-center mt-2 text-sm text-neutral-400">{launchStep}</div>
                  </div>
                )}
              </div>

              <div className="mt-6 bg-neutral-800 border border-neutral-700 rounded-lg p-6 shadow-xl">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Resumen
                </h3>
                <div className="space-y-3 text-sm text-neutral-400">
                  <div className="flex justify-between">
                    <span>Última sesión:</span>
                    <span>Hace 2 horas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Tiempo jugado:</span>
                    <span>124 horas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Mundos:</span>
                    <span>8</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 shadow-xl">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Información del Juego
                </h3>
                <div className="space-y-3 text-sm text-neutral-400">
                  <div className="flex items-center gap-3">
                    <span className="w-4 h-4 bg-green-500 rounded-full animate-pulse"></span>
                    <span>Conexión estable</span>
                  </div>
                  <div>
                    <div className="text-xs text-neutral-500 mb-1">Java Runtime</div>
                    <div className="font-mono">OpenJDK 21.0.1</div>
                  </div>
                  <div>
                    <div className="text-xs text-neutral-500 mb-1">DirectX</div>
                    <div className="font-mono">v12</div>
                  </div>
                </div>
              </div>

              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 shadow-xl">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  Estadísticas
                </h3>
                <div className="space-y-3 text-sm text-neutral-400">
                  <div className="flex justify-between">
                    <span>Kills:</span>
                    <span className="text-red-400">1,234</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Muertes:</span>
                    <span className="text-yellow-400">456</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Playtime:</span>
                    <span className="text-green-400">124h</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'servers' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h2 className="text-2xl font-bold">Servidores Recomendados</h2>
              
              {servers.map((server, index) => (
                <div 
                  key={index} 
                  className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 hover:border-blue-500/50 transition-all cursor-pointer group"
                  onClick={() => console.log('Conectando al servidor:', server.ip)}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-2xl group-hover:scale-110 transition-transform">
                      {server.name.charAt(0)}
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-lg">{server.name}</div>
                      <div className="text-sm text-neutral-400 font-mono">{server.ip}</div>
                      <div className="text-xs text-green-400 mt-1">
                        <span className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                          {server.players} jugadores
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}

              <div className="bg-neutral-800 border-2 border-dashed border-neutral-700 rounded-lg p-6 text-center">
                <button className="text-blue-400 hover:text-blue-300 font-medium">
                  <svg className="w-6 h-6 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  <div>Añadir Servidor</div>
                </button>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-2xl font-bold">Favoritos</h2>
              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6 text-center text-neutral-400">
                <svg className="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>No tienes servidores favoritos</div>
                <div className="text-sm mt-1">Haz clic en el corazón para guardar</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'news' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h2 className="text-2xl font-bold">Noticias Recientes</h2>
              
              {news.map((item, index) => (
                <div 
                  key={index} 
                  className="bg-neutral-800 border border-neutral-700 rounded-lg overflow-hidden hover:border-blue-500/50 transition-all"
                >
                  <div className="relative h-48 overflow-hidden">
                    <img 
                      src={item.image} 
                      alt={item.title} 
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                    <div className="absolute bottom-3 left-3 text-sm text-neutral-300">
                      {item.date}
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="font-semibold text-lg mb-2">{item.title}</div>
                    <div className="text-neutral-400 text-sm mb-4">
                      ¡La última actualización de Minecraft está aquí! Descubre nuevas mecánicas, bloques y criaturas que transformarán tu experiencia de juego.
                    </div>
                    <button className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-2">
                      Leer más
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="space-y-6">
              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Versiones
                </h3>
                <div className="space-y-2">
                  {['1.21.1', '1.21', '1.20.5', '1.20.4'].map((version, index) => (
                    <div 
                      key={index} 
                      className="flex items-center justify-between p-3 bg-neutral-900 rounded-lg hover:bg-neutral-700 transition-all cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                        <span className="font-mono">{version}</span>
                      </div>
                      <span className="text-xs text-neutral-400">Recomendado</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Comentarios
                </h3>
                <div className="space-y-4">
                  <div className="p-3 bg-neutral-900 rounded-lg text-sm">
                    <div className="font-medium">Player123</div>
                    <div className="text-neutral-400 mt-1">¡La nueva actualización es increíble!</div>
                    <div className="text-xs text-neutral-500 mt-1">Hace 2 horas</div>
                  </div>
                  <div className="p-3 bg-neutral-900 rounded-lg text-sm">
                    <div className="font-medium">BuilderPro</div>
                    <div className="text-neutral-400 mt-1">Los nuevos bloques de construcción son geniales</div>
                    <div className="text-xs text-neutral-500 mt-1">Hace 5 horas</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {isSettingsOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-neutral-800 border border-neutral-700 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="p-6 border-b border-neutral-700 flex items-center justify-between">
              <h2 className="text-xl font-bold">Ajustes</h2>
              <button 
                onClick={() => setIsSettingsOpen(false)}
                className="p-2 hover:bg-neutral-700 rounded-lg transition-all"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="p-6 space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                  Memoria RAM
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">RAM Mínima: {settings.ram.min}GB</label>
                    <input
                      type="range"
                      min="1"
                      max="32"
                      value={settings.ram.min}
                      onChange={(e) => handleRamChange('min', parseInt(e.target.value))}
                      className="w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">RAM Máxima: {settings.ram.max}GB</label>
                    <input
                      type="range"
                      min="1"
                      max="32"
                      value={settings.ram.max}
                      onChange={(e) => handleRamChange('max', parseInt(e.target.value))}
                      className="w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Resolución
                </h3>
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <div className="flex-1">
                      <label className="block text-sm font-medium mb-2">Ancho</label>
                      <input
                        type="number"
                        value={settings.resolution.width}
                        onChange={(e) => handleResolutionChange(parseInt(e.target.value), settings.resolution.height)}
                        className="w-full px-3 py-2 bg-neutral-900 border border-neutral-700 rounded-lg focus:outline-none focus:border-blue-500"
                      />
                    </div>
                    <div className="flex-1">
                      <label className="block text-sm font-medium mb-2">Alto</label>
                      <input
                        type="number"
                        value={settings.resolution.height}
                        onChange={(e) => handleResolutionChange(settings.resolution.width, parseInt(e.target.value))}
                        className="w-full px-3 py-2 bg-neutral-900 border border-neutral-700 rounded-lg focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.fullscreen}
                      onChange={(e) => setSettings({ ...settings, fullscreen: e.target.checked })}
                      className="w-5 h-5 rounded border-neutral-700 text-blue-600 focus:ring-blue-500"
                    />
                    <span>Modo Pantalla Completa</span>
                  </label>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Rendimiento
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">FPS Máximos</label>
                    <select
                      value={settings.maxFps}
                      onChange={(e) => setSettings({ ...settings, maxFps: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 bg-neutral-900 border border-neutral-700 rounded-lg focus:outline-none focus:border-blue-500"
                    >
                      <option value={30}>30 FPS</option>
                      <option value={60}>60 FPS</option>
                      <option value={120}>120 FPS</option>
                      <option value={144}>144 FPS</option>
                      <option value={240}>240 FPS</option>
                      <option value={9999}>Ilimitado</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Distancia de Renderizado: {settings.renderDistance} Chunks</label>
                    <input
                      type="range"
                      min="2"
                      max="32"
                      value={settings.renderDistance}
                      onChange={(e) => setSettings({ ...settings, renderDistance: parseInt(e.target.value) })}
                      className="w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  Java
                </h3>
                <div>
                  <label className="block text-sm font-medium mb-2">Ruta del ejecutable de Java</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={settings.javaPath}
                      onChange={(e) => setSettings({ ...settings, javaPath: e.target.value })}
                      className="flex-1 px-3 py-2 bg-neutral-900 border border-neutral-700 rounded-lg focus:outline-none focus:border-blue-500"
                    />
                    <button className="px-4 py-2 bg-neutral-700 hover:bg-neutral-600 rounded-lg transition-all">
                      Buscar
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-neutral-700 flex justify-end gap-3">
              <button 
                onClick={() => setIsSettingsOpen(false)}
                className="px-4 py-2 text-neutral-400 hover:text-white transition-all"
              >
                Cancelar
              </button>
              <button 
                onClick={() => setIsSettingsOpen(false)}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all"
              >
                Aceptar
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx global>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
        .slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
      `}</style>
    </div>
  );
}