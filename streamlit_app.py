import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="NFT Token Gated Content",
    page_icon="🔐",
    layout="centered"
)

# Estilo CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .exclusive-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuración
NFT_CONTRACT_ADDRESS = "0xF4820467171695F4d2760614C77503147A9CB1E8"
CHAIN_ID = 42161
CHAIN_ID_HEX = "0xa4b1"

# Título
st.markdown('<h1 class="main-title">🔐 Contenido Exclusivo NFT</h1>', unsafe_allow_html=True)

# Información
with st.expander("ℹ️ Información del NFT Requerido"):
    st.write(f"**Red:** Arbitrum One")
    st.write(f"**Contrato:** `{NFT_CONTRACT_ADDRESS}`")
    st.write(f"**Chain ID:** {CHAIN_ID}")
    st.write(f"**Requisito:** Poseer al menos 1 NFT de esta colección")

# Estado de sesión
if 'nft_verified' not in st.session_state:
    st.session_state.nft_verified = False
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = None
if 'nft_balance' not in st.session_state:
    st.session_state.nft_balance = 0

# JavaScript mejorado con detección multi-wallet
web3_component = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/web3@1.8.0/dist/web3.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 20px;
            background: transparent;
        }}
        .container {{
            max-width: 700px;
            margin: 0 auto;
        }}
        .wallet-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }}
        .wallet-button {{
            background: white;
            border: 2px solid #e0e0e0;
            padding: 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
        }}
        .wallet-button:hover {{
            border-color: #667eea;
            background: #f8f9ff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }}
        .wallet-button:active {{
            transform: translateY(0);
        }}
        .wallet-button.disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .wallet-button.disabled:hover {{
            transform: none;
            border-color: #e0e0e0;
            background: white;
        }}
        .wallet-icon {{
            font-size: 32px;
            margin-bottom: 8px;
        }}
        .button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        .button:disabled {{
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}
        .status {{
            margin: 15px 0;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.6;
        }}
        .status-info {{
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }}
        .status-success {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .status-error {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        .wallet-info {{
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 13px;
            border: 2px solid #667eea;
        }}
        .wallet-address {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            word-break: break-all;
            margin-top: 5px;
        }}
        .spinner {{
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0 10px 0;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div id="app">
            <div id="walletSelector" style="display:none;">
                <div class="section-title">🦊 Selecciona tu Wallet:</div>
                <div class="wallet-grid" id="walletGrid"></div>
            </div>
            
            <button id="detectBtn" class="button">🔍 Detectar Wallets Instaladas</button>
            <button id="verifyBtn" class="button" style="display:none;" disabled>🔍 Verificar Propiedad del NFT</button>
            
            <div id="status"></div>
            <div id="walletInfo"></div>
        </div>
    </div>

    <script>
        const NFT_ADDRESS = '{NFT_CONTRACT_ADDRESS}';
        const ARBITRUM_RPC = 'https://arb1.arbitrum.io/rpc';
        const CHAIN_ID = {CHAIN_ID};
        const CHAIN_ID_HEX = '{CHAIN_ID_HEX}';
        
        const ERC721_ABI = [{{"inputs": [{{"internalType": "address", "name": "owner", "type": "address"}}], "name": "balanceOf", "outputs": [{{"internalType": "uint256", "name": "", "type": "uint256"}}], "stateMutability": "view", "type": "function"}}];
        
        let web3;
        let userAddress;
        let selectedProvider = null;

        const detectBtn = document.getElementById('detectBtn');
        const verifyBtn = document.getElementById('verifyBtn');
        const statusDiv = document.getElementById('status');
        const walletInfoDiv = document.getElementById('walletInfo');
        const walletSelector = document.getElementById('walletSelector');
        const walletGrid = document.getElementById('walletGrid');

        // Configuración de wallets conocidas
        const WALLETS = {{
            'isMetaMask': {{ name: 'MetaMask', icon: '🦊', priority: 1 }},
            'isRabby': {{ name: 'Rabby', icon: '🐰', priority: 2 }},
            'isOkxWallet': {{ name: 'OKX Wallet', icon: '⭕', priority: 3 }},
            'isPhantom': {{ name: 'Phantom', icon: '👻', priority: 4 }},
            'isBraveWallet': {{ name: 'Brave Wallet', icon: '🦁', priority: 5 }},
            'isCoinbaseWallet': {{ name: 'Coinbase', icon: '🔵', priority: 6 }},
            'isTrust': {{ name: 'Trust Wallet', icon: '🛡️', priority: 7 }}
        }};

        function showStatus(message, type) {{
            const spinner = type === 'info' ? '<span class="spinner"></span>' : '';
            statusDiv.className = `status status-${{type}}`;
            statusDiv.innerHTML = spinner + message;
            statusDiv.style.display = 'block';
        }}

        function getAvailableWallets() {{
            const available = [];
            
            // Comprobar window.ethereum y sus proveedores
            if (typeof window.ethereum !== 'undefined') {{
                // Si hay múltiples proveedores (EIP-6963 o providers array)
                if (window.ethereum.providers && Array.isArray(window.ethereum.providers)) {{
                    window.ethereum.providers.forEach((provider, index) => {{
                        for (const [key, wallet] of Object.entries(WALLETS)) {{
                            if (provider[key]) {{
                                available.push({{
                                    provider: provider,
                                    ...wallet,
                                    index: index
                                }});
                                break;
                            }}
                        }}
                    }});
                }} else {{
                    // Proveedor único, detectar cuál es
                    for (const [key, wallet] of Object.entries(WALLETS)) {{
                        if (window.ethereum[key]) {{
                            available.push({{
                                provider: window.ethereum,
                                ...wallet,
                                index: 0
                            }});
                            break;
                        }}
                    }}
                    
                    // Si no se detectó ninguna, usar como genérica
                    if (available.length === 0) {{
                        available.push({{
                            provider: window.ethereum,
                            name: 'Wallet Detectada',
                            icon: '💼',
                            priority: 99,
                            index: 0
                        }});
                    }}
                }}
            }}
            
            // Comprobar wallets específicas en sus propios objetos
            if (typeof window.rabby !== 'undefined') {{
                available.push({{
                    provider: window.rabby,
                    name: 'Rabby',
                    icon: '🐰',
                    priority: 2,
                    index: available.length
                }});
            }}
            
            if (typeof window.okxwallet !== 'undefined') {{
                available.push({{
                    provider: window.okxwallet,
                    name: 'OKX Wallet',
                    icon: '⭕',
                    priority: 3,
                    index: available.length
                }});
            }}

            if (typeof window.phantom?.ethereum !== 'undefined') {{
                available.push({{
                    provider: window.phantom.ethereum,
                    name: 'Phantom',
                    icon: '👻',
                    priority: 4,
                    index: available.length
                }});
            }}
            
            return available.sort((a, b) => a.priority - b.priority);
        }}

        detectBtn.addEventListener('click', () => {{
            const wallets = getAvailableWallets();
            
            if (wallets.length === 0) {{
                showStatus('⚠️ No se detectaron wallets. Por favor, instala MetaMask, Rabby u otra wallet compatible.', 'error');
                return;
            }}
            
            if (wallets.length === 1) {{
                // Solo una wallet, conectar directamente
                selectedProvider = wallets[0].provider;
                showStatus(`✅ Detectada: ${{wallets[0].name}}. Conectando...`, 'info');
                connectWallet();
            }} else {{
                // Múltiples wallets, mostrar selector
                walletGrid.innerHTML = '';
                wallets.forEach(wallet => {{
                    const button = document.createElement('div');
                    button.className = 'wallet-button';
                    button.innerHTML = `
                        <div class="wallet-icon">${{wallet.icon}}</div>
                        <div>${{wallet.name}}</div>
                    `;
                    button.onclick = () => {{
                        selectedProvider = wallet.provider;
                        showStatus(`Conectando con ${{wallet.name}}...`, 'info');
                        walletSelector.style.display = 'none';
                        detectBtn.style.display = 'none';
                        connectWallet();
                    }};
                    walletGrid.appendChild(button);
                }});
                
                walletSelector.style.display = 'block';
                detectBtn.style.display = 'none';
                showStatus(`✅ Detectadas ${{wallets.length}} wallets. Selecciona una para continuar.`, 'success');
            }}
        }});

        async function switchToArbitrum() {{
            try {{
                await selectedProvider.request({{
                    method: 'wallet_switchEthereumChain',
                    params: [{{ chainId: CHAIN_ID_HEX }}],
                }});
                return true;
            }} catch (switchError) {{
                if (switchError.code === 4902) {{
                    try {{
                        await selectedProvider.request({{
                            method: 'wallet_addEthereumChain',
                            params: [{{
                                chainId: CHAIN_ID_HEX,
                                chainName: 'Arbitrum One',
                                nativeCurrency: {{ 
                                    name: 'Ethereum', 
                                    symbol: 'ETH', 
                                    decimals: 18 
                                }},
                                rpcUrls: ['https://arb1.arbitrum.io/rpc'],
                                blockExplorerUrls: ['https://arbiscan.io/']
                            }}]
                        }});
                        return true;
                    }} catch (addError) {{
                        console.error('Error al agregar red:', addError);
                        return false;
                    }}
                }}
                console.error('Error al cambiar de red:', switchError);
                return false;
            }}
        }}

        async function connectWallet() {{
            try {{
                showStatus('🔄 Solicitando acceso a la wallet...', 'info');
                
                const accounts = await selectedProvider.request({{ 
                    method: 'eth_requestAccounts' 
                }});
                
                if (!accounts || accounts.length === 0) {{
                    throw new Error('No se pudo obtener acceso a la wallet');
                }}
                
                userAddress = accounts[0];
                console.log('Cuenta conectada:', userAddress);
                
                showStatus('🔄 Cambiando a la red Arbitrum...', 'info');
                const switched = await switchToArbitrum();
                
                if (!switched) {{
                    showStatus('⚠️ Por favor, cambia manualmente a Arbitrum en tu wallet.', 'error');
                    detectBtn.style.display = 'block';
                    return;
                }}

                web3 = new Web3(selectedProvider);
                
                walletInfoDiv.className = 'wallet-info';
                walletInfoDiv.innerHTML = `
                    <div>✅ <strong>Wallet Conectada</strong></div>
                    <div class="wallet-address">${{userAddress}}</div>
                `;
                
                verifyBtn.style.display = 'block';
                verifyBtn.disabled = false;
                
                showStatus('✅ Conexión exitosa. Ahora puedes verificar tu NFT.', 'success');
                
            }} catch (error) {{
                console.error('Error de conexión:', error);
                showStatus(`❌ Error: ${{error.message}}`, 'error');
                detectBtn.style.display = 'block';
                walletSelector.style.display = 'none';
            }}
        }}

        verifyBtn.addEventListener('click', async () => {{
            try {{
                verifyBtn.disabled = true;
                showStatus('🔄 Preparando verificación...', 'info');

                const timestamp = Date.now();
                const message = `Verificar propiedad de NFT\\n\\nWallet: ${{userAddress}}\\nContrato: ${{NFT_ADDRESS}}\\nRed: Arbitrum One\\nTimestamp: ${{timestamp}}\\n\\nEsta firma es gratuita y no autoriza transacciones.`;

                showStatus('✍️ Por favor, firma el mensaje en tu wallet...', 'info');
                const signature = await web3.eth.personal.sign(message, userAddress);
                console.log('Firmado:', signature);

                showStatus('🔍 Consultando balance del NFT...', 'info');
                const arbitrumWeb3 = new Web3(ARBITRUM_RPC);
                const contract = new arbitrumWeb3.eth.Contract(ERC721_ABI, NFT_ADDRESS);
                
                const balance = await contract.methods.balanceOf(userAddress).call();
                const balanceNum = parseInt(balance);
                
                if (balanceNum > 0) {{
                    showStatus(`✅ ¡Verificación exitosa! Posees ${{balanceNum}} NFT(s).`, 'success');
                    
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{
                            success: true,
                            address: userAddress,
                            balance: balanceNum
                        }}
                    }}, '*');
                    
                }} else {{
                    showStatus('❌ No posees ningún NFT de esta colección.', 'error');
                    
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{
                            success: false,
                            address: userAddress,
                            balance: 0
                        }}
                    }}, '*');
                }}

            }} catch (error) {{
                console.error('Error:', error);
                let errorMsg = error.message;
                
                if (error.code === 4001 || errorMsg.includes('User denied')) {{
                    errorMsg = 'Firma cancelada por el usuario.';
                }}
                
                showStatus(`❌ Error: ${{errorMsg}}`, 'error');
            }} finally {{
                verifyBtn.disabled = false;
            }}
        }});

        // Auto-detectar al cargar
        window.addEventListener('load', () => {{
            setTimeout(() => {{
                const wallets = getAvailableWallets();
                if (wallets.length > 0) {{
                    showStatus(`💼 ${{wallets.length}} wallet(s) detectada(s). Haz clic en "Detectar Wallets" para continuar.`, 'info');
                }} else {{
                    showStatus('⚠️ No se detectaron wallets. Instala MetaMask, Rabby u otra wallet compatible.', 'error');
                }}
            }}, 500);
        }});
    </script>
</body>
</html>
"""

# Renderizar componente Web3
verification_result = components.html(web3_component, height=600, scrolling=True)

# Procesar resultado
if verification_result:
    if isinstance(verification_result, dict):
        if verification_result.get('success'):
            st.session_state.nft_verified = True
            st.session_state.wallet_address = verification_result.get('address')
            st.session_state.nft_balance = verification_result.get('balance', 0)
        else:
            st.session_state.nft_verified = False

st.markdown("---")

# Sección de contenido
st.markdown("### 📄 Acceso al Contenido")

# Botones de simulación
col1, col2 = st.columns(2)
with col1:
    if st.button("🔓 Simular Verificación (Prueba)"):
        st.session_state.nft_verified = True
        st.session_state.wallet_address = "0x1234...5678"
        st.session_state.nft_balance = 1
        st.rerun()

with col2:
    if st.button("🔒 Resetear"):
        st.session_state.nft_verified = False
        st.session_state.wallet_address = None
        st.session_state.nft_balance = 0
        st.rerun()

st.markdown("---")

# Mostrar contenido
if st.session_state.nft_verified:
    st.markdown("""
    <div class="exclusive-content">
        <h2>🎉 ¡Contenido Exclusivo Desbloqueado!</h2>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Felicidades por ser parte de nuestra comunidad de NFT holders.
        </p>
        <hr style="border-color: rgba(255,255,255,0.3); margin: 1.5rem 0;">
        <h3>📚 Contenido Premium</h3>
        <ul style="font-size: 1rem; line-height: 1.8;">
            <li>✨ Acceso a materiales educativos exclusivos</li>
            <li>🎪 Participación en eventos privados</li>
            <li>🚀 Ventajas en futuros lanzamientos</li>
            <li>💬 Comunicación directa con el equipo</li>
            <li>🗳️ Votación en decisiones del proyecto</li>
        </ul>
        <p style="margin-top: 1.5rem; font-style: italic;">
            💎 Gracias por tu apoyo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.wallet_address:
        st.success(f"✅ Verificado: `{st.session_state.wallet_address}`")
        st.info(f"🎫 NFTs: **{st.session_state.nft_balance}**")

else:
    st.markdown("""
    <div class="error-box">
        <h3>🔒 Contenido Exclusivo para Token Holders</h3>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Este contenido está reservado para poseedores de NFTs de nuestra colección.
        </p>
        <p style="margin-top: 1rem;"><strong>Para acceder necesitas:</strong></p>
        <ul style="margin-left: 1.5rem;">
            <li>Poseer al menos 1 NFT del contrato</li>
            <li>Tener una wallet Web3 instalada</li>
            <li>Conectar y firmar (sin coste)</li>
        </ul>
        <p style="margin-top: 1.5rem; font-weight: bold;">
            👆 Usa "Detectar Wallets" arriba para comenzar.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    <p>🔐 Verificación offchain | Sin costes | Multi-Wallet</p>
    <p style="font-size: 0.8rem;">Soporta: MetaMask, Rabby, OKX, Phantom, Brave Wallet, Coinbase y más</p>
</div>
""", unsafe_allow_html=True)
