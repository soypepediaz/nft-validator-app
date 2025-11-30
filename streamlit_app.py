import streamlit as st
import streamlit.components.v1 as components
import json

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
if 'wallet_connected' not in st.session_state:
    st.session_state.wallet_connected = False
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = None
if 'nft_verified' not in st.session_state:
    st.session_state.nft_verified = False
if 'nft_balance' not in st.session_state:
    st.session_state.nft_balance = 0

# JavaScript para Web3 - VERSIÓN FULLSCREEN (sin iframe restrictions)
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
            max-width: 600px;
            margin: 0 auto;
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
        .button:active {{
            transform: translateY(0);
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
    </style>
</head>
<body>
    <div class="container">
        <div id="app">
            <button id="connectBtn" class="button">🦊 Conectar con MetaMask</button>
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

        const connectBtn = document.getElementById('connectBtn');
        const verifyBtn = document.getElementById('verifyBtn');
        const statusDiv = document.getElementById('status');
        const walletInfoDiv = document.getElementById('walletInfo');

        function showStatus(message, type) {{
            const spinner = type === 'info' ? '<span class="spinner"></span>' : '';
            statusDiv.className = `status status-${{type}}`;
            statusDiv.innerHTML = spinner + message;
            statusDiv.style.display = 'block';
        }}

        function hideStatus() {{
            statusDiv.style.display = 'none';
        }}

        // Detectar MetaMask al cargar
        window.addEventListener('load', () => {{
            if (typeof window.ethereum === 'undefined') {{
                showStatus('⚠️ MetaMask no está instalado. Por favor, instala MetaMask para continuar.', 'error');
                connectBtn.disabled = true;
            }} else {{
                showStatus('✅ MetaMask detectado. Haz clic en "Conectar" para comenzar.', 'info');
            }}
        }});

        async function switchToArbitrum() {{
            try {{
                await window.ethereum.request({{
                    method: 'wallet_switchEthereumChain',
                    params: [{{ chainId: CHAIN_ID_HEX }}],
                }});
                return true;
            }} catch (switchError) {{
                if (switchError.code === 4902) {{
                    try {{
                        await window.ethereum.request({{
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

        connectBtn.addEventListener('click', async () => {{
            if (typeof window.ethereum === 'undefined') {{
                showStatus('⚠️ MetaMask no detectado. Por favor, instala MetaMask.', 'error');
                return;
            }}

            try {{
                connectBtn.disabled = true;
                showStatus('🔄 Solicitando acceso a MetaMask...', 'info');
                
                // Solicitar cuentas
                const accounts = await window.ethereum.request({{ 
                    method: 'eth_requestAccounts' 
                }});
                
                if (!accounts || accounts.length === 0) {{
                    throw new Error('No se pudo obtener acceso a la wallet');
                }}
                
                userAddress = accounts[0];
                console.log('Cuenta conectada:', userAddress);
                
                // Cambiar a Arbitrum
                showStatus('🔄 Cambiando a la red Arbitrum...', 'info');
                const switched = await switchToArbitrum();
                
                if (!switched) {{
                    showStatus('⚠️ No se pudo cambiar a Arbitrum. Por favor, cámbiala manualmente en MetaMask.', 'error');
                    connectBtn.disabled = false;
                    return;
                }}

                // Inicializar Web3
                web3 = new Web3(window.ethereum);
                
                // Mostrar información de wallet
                walletInfoDiv.className = 'wallet-info';
                walletInfoDiv.innerHTML = `
                    <div>✅ <strong>Wallet Conectada</strong></div>
                    <div class="wallet-address">${{userAddress}}</div>
                `;
                
                // Ocultar botón de conectar y mostrar botón de verificar
                connectBtn.style.display = 'none';
                verifyBtn.style.display = 'block';
                verifyBtn.disabled = false;
                
                showStatus('✅ Conexión exitosa. Ahora puedes verificar tu NFT.', 'success');
                
            }} catch (error) {{
                console.error('Error de conexión:', error);
                showStatus(`❌ Error: ${{error.message}}`, 'error');
                connectBtn.disabled = false;
            }}
        }});

        verifyBtn.addEventListener('click', async () => {{
            try {{
                verifyBtn.disabled = true;
                showStatus('🔄 Preparando mensaje de verificación...', 'info');

                // Crear mensaje para firmar
                const timestamp = Date.now();
                const message = `Verificar propiedad de NFT\\n\\nWallet: ${{userAddress}}\\nContrato: ${{NFT_ADDRESS}}\\nRed: Arbitrum One\\nTimestamp: ${{timestamp}}\\n\\nEsta firma es gratuita y no autoriza transacciones.`;

                // Solicitar firma
                showStatus('✍️ Por favor, firma el mensaje en MetaMask...', 'info');
                const signature = await web3.eth.personal.sign(message, userAddress);
                console.log('Mensaje firmado:', signature);

                // Verificar balance del NFT
                showStatus('🔍 Consultando balance del NFT en Arbitrum...', 'info');
                const arbitrumWeb3 = new Web3(ARBITRUM_RPC);
                const contract = new arbitrumWeb3.eth.Contract(ERC721_ABI, NFT_ADDRESS);
                
                const balance = await contract.methods.balanceOf(userAddress).call();
                console.log('Balance NFT:', balance);
                
                const balanceNum = parseInt(balance);
                
                if (balanceNum > 0) {{
                    showStatus(`✅ ¡Verificación exitosa! Posees ${{balanceNum}} NFT(s) de esta colección.`, 'success');
                    
                    // Notificar a Streamlit
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
                    
                    // Notificar a Streamlit
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
                console.error('Error en verificación:', error);
                let errorMsg = error.message;
                
                if (error.code === 4001) {{
                    errorMsg = 'Firma cancelada por el usuario.';
                }} else if (errorMsg.includes('User denied')) {{
                    errorMsg = 'Firma rechazada. Por favor, acepta la firma en MetaMask.';
                }}
                
                showStatus(`❌ Error: ${{errorMsg}}`, 'error');
            }} finally {{
                verifyBtn.disabled = false;
            }}
        }});

        // Listeners para cambios en MetaMask
        if (window.ethereum) {{
            window.ethereum.on('accountsChanged', (accounts) => {{
                if (accounts.length === 0) {{
                    location.reload();
                }} else {{
                    userAddress = accounts[0];
                    if (walletInfoDiv) {{
                        walletInfoDiv.innerHTML = `
                            <div>✅ <strong>Wallet Conectada</strong></div>
                            <div class="wallet-address">${{userAddress}}</div>
                        `;
                    }}
                    showStatus('🔄 Cuenta cambiada. Por favor, verifica nuevamente.', 'info');
                }}
            }});

            window.ethereum.on('chainChanged', () => {{
                location.reload();
            }});
        }}
    </script>
</body>
</html>
"""

# Renderizar componente Web3
verification_result = components.html(web3_component, height=500, scrolling=True)

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

# Botones de simulación para pruebas
col1, col2 = st.columns(2)
with col1:
    if st.button("🔓 Simular Verificación (Prueba)", help="Solo para testing"):
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

# Mostrar contenido según verificación
if st.session_state.nft_verified:
    st.markdown("""
    <div class="exclusive-content">
        <h2>🎉 ¡Contenido Exclusivo Desbloqueado!</h2>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Felicidades por ser parte de nuestra comunidad de NFT holders. 
            Este es contenido exclusivo solo para miembros verificados.
        </p>
        <hr style="border-color: rgba(255,255,255,0.3); margin: 1.5rem 0;">
        <h3>📚 Contenido Premium</h3>
        <ul style="font-size: 1rem; line-height: 1.8;">
            <li>✨ Acceso a materiales educativos exclusivos</li>
            <li>🎪 Participación en eventos privados de la comunidad</li>
            <li>🚀 Ventajas especiales en futuros lanzamientos</li>
            <li>💬 Comunicación directa con el equipo fundador</li>
            <li>🗳️ Votación en decisiones importantes del proyecto</li>
        </ul>
        <p style="margin-top: 1.5rem; font-style: italic; opacity: 0.9;">
            💎 Gracias por tu apoyo y confianza en nuestro proyecto.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.wallet_address:
        st.success(f"✅ Verificado con wallet: `{st.session_state.wallet_address}`")
        st.info(f"🎫 NFTs en posesión: **{st.session_state.nft_balance}**")

else:
    st.markdown("""
    <div class="error-box">
        <h3>🔒 Contenido Exclusivo para Token Holders</h3>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Este contenido está reservado exclusivamente para los poseedores de NFTs 
            de nuestra colección en la red Arbitrum.
        </p>
        <p style="margin-top: 1rem;">
            <strong>Para acceder necesitas:</strong>
        </p>
        <ul style="margin-top: 0.5rem; margin-left: 1.5rem;">
            <li>Poseer al menos 1 NFT del contrato especificado</li>
            <li>Tener MetaMask u otra wallet Web3 instalada</li>
            <li>Conectar tu wallet usando el botón de arriba</li>
            <li>Firmar un mensaje de verificación (sin coste de gas)</li>
        </ul>
        <p style="margin-top: 1.5rem; font-weight: bold;">
            👆 Usa el botón "Conectar con MetaMask" arriba para comenzar la verificación.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    <p>🔐 Verificación segura mediante firma offchain | Sin costes de gas</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">
        Powered by Web3.js & Streamlit | Arbitrum Network
    </p>
</div>
""", unsafe_allow_html=True)
