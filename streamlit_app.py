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
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ffeeba;
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

st.markdown("""
<div class="warning-box">
    <strong>🐰 Wallet Requerida:</strong> Esta aplicación está configurada para funcionar <strong>SOLO con Rabby Wallet</strong>.
    <br><br>
    Si tienes otras wallets instaladas (MetaMask, OKX, Phantom, Brave Wallet), por favor <strong>desactívalas temporalmente</strong> 
    en <code>brave://extensions/</code> o en la configuración de extensiones de tu navegador.
</div>
""", unsafe_allow_html=True)

# Información
with st.expander("ℹ️ Información del NFT Requerido"):
    st.write(f"**Red:** Arbitrum One")
    st.write(f"**Contrato:** `{NFT_CONTRACT_ADDRESS}`")
    st.write(f"**Chain ID:** {CHAIN_ID}")
    st.write(f"**Requisito:** Poseer al menos 1 NFT de esta colección")
    st.write(f"**Wallet:** Solo Rabby Wallet")

# Estado de sesión
if 'nft_verified' not in st.session_state:
    st.session_state.nft_verified = False
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = None
if 'nft_balance' not in st.session_state:
    st.session_state.nft_balance = 0

# JavaScript específico para Rabby
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
        .button {{
            background: linear-gradient(135deg, #8697FF 0%, #7C5AFF 100%);
            color: white;
            border: none;
            padding: 18px 35px;
            font-size: 17px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(134, 151, 255, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(134, 151, 255, 0.6);
        }}
        .button:active {{
            transform: translateY(0);
        }}
        .button:disabled {{
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}
        .rabby-logo {{
            width: 28px;
            height: 28px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        .status {{
            margin: 15px 0;
            padding: 18px;
            border-radius: 10px;
            font-size: 15px;
            line-height: 1.7;
        }}
        .status-info {{
            background-color: #d1ecf1;
            color: #0c5460;
            border: 2px solid #bee5eb;
        }}
        .status-success {{
            background-color: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }}
        .status-error {{
            background-color: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }}
        .status-warning {{
            background-color: #fff3cd;
            color: #856404;
            border: 2px solid #ffeeba;
        }}
        .wallet-info {{
            background: linear-gradient(135deg, #8697FF15 0%, #7C5AFF15 100%);
            padding: 18px;
            border-radius: 10px;
            margin: 15px 0;
            font-size: 14px;
            border: 2px solid #8697FF;
        }}
        .wallet-address {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            word-break: break-all;
            margin-top: 8px;
            font-size: 13px;
        }}
        .spinner {{
            border: 3px solid #f3f3f3;
            border-top: 3px solid #8697FF;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .debug-info {{
            background: #f5f5f5;
            padding: 12px;
            border-radius: 6px;
            font-size: 12px;
            font-family: monospace;
            margin: 10px 0;
            max-height: 150px;
            overflow-y: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div id="app">
            <button id="connectBtn" class="button">
                <span class="rabby-logo">🐰</span>
                <span>Conectar con Rabby Wallet</span>
            </button>
            <button id="verifyBtn" class="button" style="display:none;" disabled>
                <span>🔍 Verificar Propiedad del NFT</span>
            </button>
            
            <div id="status"></div>
            <div id="walletInfo"></div>
            <div id="debug" class="debug-info" style="display:none;"></div>
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
        let rabbyProvider = null;

        const connectBtn = document.getElementById('connectBtn');
        const verifyBtn = document.getElementById('verifyBtn');
        const statusDiv = document.getElementById('status');
        const walletInfoDiv = document.getElementById('walletInfo');
        const debugDiv = document.getElementById('debug');

        function showStatus(message, type) {{
            const spinner = type === 'info' ? '<span class="spinner"></span>' : '';
            statusDiv.className = `status status-${{type}}`;
            statusDiv.innerHTML = spinner + message;
            statusDiv.style.display = 'block';
        }}

        function addDebug(message) {{
            const timestamp = new Date().toLocaleTimeString();
            debugDiv.innerHTML += `[${{timestamp}}] ${{message}}<br>`;
            debugDiv.style.display = 'block';
            debugDiv.scrollTop = debugDiv.scrollHeight;
            console.log(`[DEBUG] ${{message}}`);
        }}

        function detectRabby() {{
            addDebug('Iniciando detección de Rabby...');
            
            // Método 1: Objeto window.rabby directo
            if (typeof window.rabby !== 'undefined') {{
                addDebug('✅ Rabby detectada en window.rabby');
                return window.rabby;
            }}
            
            // Método 2: window.ethereum con flag isRabby
            if (typeof window.ethereum !== 'undefined') {{
                addDebug('window.ethereum existe, verificando...');
                
                if (window.ethereum.isRabby) {{
                    addDebug('✅ Rabby detectada en window.ethereum.isRabby');
                    return window.ethereum;
                }}
                
                // Método 3: Array de proveedores
                if (window.ethereum.providers && Array.isArray(window.ethereum.providers)) {{
                    addDebug(`Detectados ${{window.ethereum.providers.length}} proveedores`);
                    for (let i = 0; i < window.ethereum.providers.length; i++) {{
                        const provider = window.ethereum.providers[i];
                        addDebug(`Proveedor ${{i}}: isRabby=${{provider.isRabby}}`);
                        if (provider.isRabby) {{
                            addDebug('✅ Rabby encontrada en array de proveedores');
                            return provider;
                        }}
                    }}
                }}
            }}
            
            addDebug('❌ Rabby no detectada');
            return null;
        }}

        // Detectar Rabby al cargar
        window.addEventListener('load', () => {{
            setTimeout(() => {{
                rabbyProvider = detectRabby();
                
                if (rabbyProvider) {{
                    showStatus('✅ Rabby Wallet detectada. Haz clic en "Conectar" para continuar.', 'success');
                }} else {{
                    showStatus('⚠️ <strong>Rabby Wallet no detectada.</strong><br><br>Por favor:<br>1. Instala Rabby desde <a href="https://rabby.io" target="_blank">rabby.io</a><br>2. Desactiva otras wallets en brave://extensions/<br>3. Refresca esta página', 'error');
                    connectBtn.disabled = true;
                }}
            }}, 800);
        }});

        async function switchToArbitrum() {{
            try {{
                addDebug('Intentando cambiar a Arbitrum...');
                await rabbyProvider.request({{
                    method: 'wallet_switchEthereumChain',
                    params: [{{ chainId: CHAIN_ID_HEX }}],
                }});
                addDebug('✅ Cambiado a Arbitrum');
                return true;
            }} catch (switchError) {{
                addDebug(`Error al cambiar: ${{switchError.code}} - ${{switchError.message}}`);
                
                if (switchError.code === 4902) {{
                    try {{
                        addDebug('Red no encontrada, agregando...');
                        await rabbyProvider.request({{
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
                        addDebug('✅ Red Arbitrum agregada');
                        return true;
                    }} catch (addError) {{
                        addDebug(`❌ Error al agregar red: ${{addError.message}}`);
                        return false;
                    }}
                }}
                return false;
            }}
        }}

        connectBtn.addEventListener('click', async () => {{
            if (!rabbyProvider) {{
                rabbyProvider = detectRabby();
                if (!rabbyProvider) {{
                    showStatus('⚠️ Rabby Wallet no encontrada. Por favor, instálala y refresca la página.', 'error');
                    return;
                }}
            }}

            try {{
                connectBtn.disabled = true;
                addDebug('Solicitando cuentas a Rabby...');
                showStatus('🔄 Abriendo Rabby Wallet... Por favor, autoriza la conexión.', 'info');
                
                const accounts = await rabbyProvider.request({{ 
                    method: 'eth_requestAccounts' 
                }});
                
                if (!accounts || accounts.length === 0) {{
                    throw new Error('No se obtuvieron cuentas de Rabby');
                }}
                
                userAddress = accounts[0];
                addDebug(`✅ Cuenta obtenida: ${{userAddress}}`);
                
                showStatus('🔄 Cambiando a la red Arbitrum en Rabby...', 'info');
                const switched = await switchToArbitrum();
                
                if (!switched) {{
                    showStatus('⚠️ No se pudo cambiar a Arbitrum. Por favor, cámbiala manualmente en Rabby.', 'warning');
                    connectBtn.disabled = false;
                    return;
                }}

                web3 = new Web3(rabbyProvider);
                addDebug('✅ Web3 inicializado con Rabby');
                
                walletInfoDiv.className = 'wallet-info';
                walletInfoDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 24px;">🐰</span>
                        <div>
                            <strong>Rabby Wallet Conectada</strong>
                            <div class="wallet-address">${{userAddress}}</div>
                        </div>
                    </div>
                `;
                
                connectBtn.style.display = 'none';
                verifyBtn.style.display = 'block';
                verifyBtn.disabled = false;
                
                showStatus('✅ Conexión exitosa con Rabby. Ahora puedes verificar tu NFT.', 'success');
                
            }} catch (error) {{
                addDebug(`❌ Error de conexión: ${{error.message}}`);
                console.error('Error completo:', error);
                
                let errorMsg = error.message;
                if (error.code === 4001 || errorMsg.includes('User rejected')) {{
                    errorMsg = 'Conexión rechazada por el usuario en Rabby.';
                }}
                
                showStatus(`❌ Error: ${{errorMsg}}`, 'error');
                connectBtn.disabled = false;
            }}
        }});

        verifyBtn.addEventListener('click', async () => {{
            try {{
                verifyBtn.disabled = true;
                addDebug('Iniciando verificación de NFT...');
                showStatus('🔄 Preparando mensaje de verificación...', 'info');

                const timestamp = Date.now();
                const message = `Verificar propiedad de NFT

Wallet: ${{userAddress}}
Contrato: ${{NFT_ADDRESS}}
Red: Arbitrum One
Timestamp: ${{timestamp}}

Esta firma es gratuita y no autoriza ninguna transacción.`;

                addDebug('Solicitando firma a Rabby...');
                showStatus('✍️ Por favor, firma el mensaje en Rabby Wallet...', 'info');
                
                const signature = await web3.eth.personal.sign(message, userAddress);
                addDebug(`✅ Mensaje firmado: ${{signature.substring(0, 20)}}...`);

                showStatus('🔍 Consultando balance del NFT en Arbitrum...', 'info');
                addDebug('Conectando a RPC de Arbitrum...');
                
                const arbitrumWeb3 = new Web3(ARBITRUM_RPC);
                const contract = new arbitrumWeb3.eth.Contract(ERC721_ABI, NFT_ADDRESS);
                
                addDebug('Llamando a balanceOf...');
                const balance = await contract.methods.balanceOf(userAddress).call();
                const balanceNum = parseInt(balance);
                addDebug(`Balance obtenido: ${{balanceNum}}`);
                
                if (balanceNum > 0) {{
                    showStatus(`✅ ¡Verificación exitosa! Posees ${{balanceNum}} NFT(s) de esta colección.`, 'success');
                    
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{
                            success: true,
                            address: userAddress,
                            balance: balanceNum,
                            signature: signature
                        }}
                    }}, '*');
                    
                }} else {{
                    showStatus('❌ No posees ningún NFT de esta colección. El acceso está restringido a holders.', 'error');
                    
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
                addDebug(`❌ Error en verificación: ${{error.message}}`);
                console.error('Error completo:', error);
                
                let errorMsg = error.message;
                
                if (error.code === 4001 || errorMsg.includes('User denied') || errorMsg.includes('User rejected')) {{
                    errorMsg = 'Firma cancelada por el usuario en Rabby.';
                }} else if (errorMsg.includes('execution reverted')) {{
                    errorMsg = 'Error al consultar el contrato. Verifica que la dirección del NFT sea correcta.';
                }}
                
                showStatus(`❌ Error: ${{errorMsg}}`, 'error');
            }} finally {{
                verifyBtn.disabled = false;
            }}
        }});

        // Listeners para cambios en Rabby
        if (rabbyProvider) {{
            rabbyProvider.on('accountsChanged', (accounts) => {{
                addDebug('Cuenta cambiada en Rabby');
                if (accounts.length === 0) {{
                    location.reload();
                }} else {{
                    userAddress = accounts[0];
                    if (walletInfoDiv) {{
                        walletInfoDiv.innerHTML = `
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 24px;">🐰</span>
                                <div>
                                    <strong>Rabby Wallet Conectada</strong>
                                    <div class="wallet-address">${{userAddress}}</div>
                                </div>
                            </div>
                        `;
                    }}
                    showStatus('🔄 Cuenta cambiada. Por favor, verifica nuevamente.', 'info');
                }}
            }});

            rabbyProvider.on('chainChanged', (chainId) => {{
                addDebug(`Red cambiada: ${{chainId}}`);
                location.reload();
            }});
        }}
    </script>
</body>
</html>
"""

# Renderizar componente Web3
verification_result = components.html(web3_component, height=650, scrolling=True)

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
        st.success(f"✅ Verificado con Rabby: `{st.session_state.wallet_address}`")
        st.info(f"🎫 NFTs en posesión: **{st.session_state.nft_balance}**")

else:
    st.markdown("""
    <div class="error-box">
        <h3>🔒 Contenido Exclusivo para Token Holders</h3>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Este contenido está reservado para poseedores de NFTs de nuestra colección.
        </p>
        <p style="margin-top: 1rem;"><strong>Para acceder necesitas:</strong></p>
        <ul style="margin-left: 1.5rem;">
            <li>Poseer al menos 1 NFT del contrato especificado</li>
            <li>Tener Rabby Wallet instalada</li>
            <li>Conectar y firmar con Rabby (sin coste)</li>
        </ul>
        <p style="margin-top: 1.5rem; font-weight: bold;">
            👆 Usa "Conectar con Rabby Wallet" arriba para comenzar.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    <p>🔐 Verificación offchain con Rabby Wallet | Sin costes de gas</p>
    <p style="font-size: 0.8rem;">Optimizado exclusivamente para Rabby | Arbitrum Network</p>
</div>
""", unsafe_allow_html=True)
