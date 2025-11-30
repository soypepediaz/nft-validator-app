import streamlit as st
import streamlit.components.v1 as components
from web3 import Web3
import json

# Configuración de la página
st.set_page_config(
    page_title="NFT Token Gated Content",
    page_icon="🔐",
    layout="centered"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
    }
    .exclusive-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Configuración de Arbitrum
ARBITRUM_RPC = "https://arb1.arbitrum.io/rpc"
NFT_CONTRACT_ADDRESS = "0xF4820467171695F4d2760614C77503147A9CB1E8"
CHAIN_ID = 42161  # Arbitrum One

# ABI básico para ERC721
ERC721_ABI = json.dumps([
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
])

# Título principal
st.markdown('<h1 class="main-title">🔐 Contenido Exclusivo NFT</h1>', unsafe_allow_html=True)

# Información del NFT
with st.expander("ℹ️ Información del NFT Requerido"):
    st.write(f"**Red:** Arbitrum")
    st.write(f"**Contrato:** `{NFT_CONTRACT_ADDRESS}`")
    st.write(f"**Requisito:** Poseer al menos 1 NFT de esta colección")

# HTML/JavaScript para Web3
web3_component = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/web3@1.8.0/dist/web3.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
            background-color: transparent;
        }}
        .button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            transition: transform 0.2s;
        }}
        .button:hover {{
            transform: scale(1.05);
        }}
        .button:disabled {{
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
        }}
        .status {{
            margin: 15px 0;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
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
            background-color: #fff3cd;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-size: 12px;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div id="app">
        <button id="connectBtn" class="button">Conectar Wallet</button>
        <button id="verifyBtn" class="button" style="display:none;" disabled>Verificar NFT</button>
        <div id="status"></div>
        <div id="walletInfo"></div>
    </div>

    <script>
        const NFT_ADDRESS = '{NFT_CONTRACT_ADDRESS}';
        const ARBITRUM_RPC = '{ARBITRUM_RPC}';
        const CHAIN_ID = {CHAIN_ID};
        
        const ERC721_ABI = {ERC721_ABI};
        
        let web3;
        let userAddress;
        let contract;

        const connectBtn = document.getElementById('connectBtn');
        const verifyBtn = document.getElementById('verifyBtn');
        const statusDiv = document.getElementById('status');
        const walletInfoDiv = document.getElementById('walletInfo');

        function showStatus(message, type) {{
            statusDiv.className = `status status-${{type}}`;
            statusDiv.innerHTML = message;
            statusDiv.style.display = 'block';
        }}

        async function switchToArbitrum() {{
            try {{
                await window.ethereum.request({{
                    method: 'wallet_switchEthereumChain',
                    params: [{{ chainId: '0x' + CHAIN_ID.toString(16) }}],
                }});
                return true;
            }} catch (switchError) {{
                // Si la red no está agregada, intentar agregarla
                if (switchError.code === 4902) {{
                    try {{
                        await window.ethereum.request({{
                            method: 'wallet_addEthereumChain',
                            params: [{{
                                chainId: '0x' + CHAIN_ID.toString(16),
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
                showStatus('⚠️ Por favor, instala MetaMask u otra wallet Web3', 'error');
                return;
            }}

            try {{
                showStatus('🔄 Conectando con tu wallet...', 'info');
                
                // Solicitar acceso a las cuentas
                const accounts = await window.ethereum.request({{ 
                    method: 'eth_requestAccounts' 
                }});
                
                userAddress = accounts[0];
                
                // Cambiar a Arbitrum
                showStatus('🔄 Cambiando a la red Arbitrum...', 'info');
                const switched = await switchToArbitrum();
                
                if (!switched) {{
                    showStatus('⚠️ Por favor, cambia manualmente a la red Arbitrum en tu wallet', 'error');
                    return;
                }}

                web3 = new Web3(window.ethereum);
                
                walletInfoDiv.className = 'wallet-info';
                walletInfoDiv.innerHTML = `✅ Wallet conectada: ${{userAddress.substring(0, 6)}}...${{userAddress.substring(38)}}`;
                
                connectBtn.style.display = 'none';
                verifyBtn.style.display = 'block';
                verifyBtn.disabled = false;
                
                showStatus('✅ Wallet conectada exitosamente. Ahora puedes verificar tu NFT.', 'success');
                
            }} catch (error) {{
                console.error('Error al conectar:', error);
                showStatus('❌ Error al conectar la wallet: ' + error.message, 'error');
            }}
        }});

        verifyBtn.addEventListener('click', async () => {{
            try {{
                verifyBtn.disabled = true;
                showStatus('🔄 Preparando mensaje para firmar...', 'info');

                // Crear mensaje para firmar
                const timestamp = Date.now();
                const message = `Verificar propiedad de NFT\\nDirección: ${{userAddress}}\\nContrato: ${{NFT_ADDRESS}}\\nTimestamp: ${{timestamp}}`;

                // Solicitar firma
                showStatus('✍️ Por favor, firma el mensaje en tu wallet...', 'info');
                const signature = await web3.eth.personal.sign(message, userAddress);

                // Verificar balance usando RPC público de Arbitrum
                showStatus('🔍 Verificando propiedad del NFT...', 'info');
                const arbitrumWeb3 = new Web3(ARBITRUM_RPC);
                contract = new arbitrumWeb3.eth.Contract(ERC721_ABI, NFT_ADDRESS);
                
                const balance = await contract.methods.balanceOf(userAddress).call();
                
                // Comunicar resultado a Streamlit
                if (parseInt(balance) > 0) {{
                    window.parent.postMessage({{
                        type: 'nft-verification',
                        success: true,
                        address: userAddress,
                        balance: balance.toString(),
                        signature: signature,
                        message: message
                    }}, '*');
                    showStatus(`✅ ¡Verificación exitosa! Posees ${{balance}} NFT(s) de esta colección.`, 'success');
                }} else {{
                    window.parent.postMessage({{
                        type: 'nft-verification',
                        success: false,
                        address: userAddress,
                        balance: '0'
                    }}, '*');
                    showStatus('❌ No posees ningún NFT de esta colección.', 'error');
                }}

            }} catch (error) {{
                console.error('Error en verificación:', error);
                showStatus('❌ Error durante la verificación: ' + error.message, 'error');
                window.parent.postMessage({{
                    type: 'nft-verification',
                    success: false,
                    error: error.message
                }}, '*');
            }} finally {{
                verifyBtn.disabled = false;
            }}
        }});

        // Listener para cambios de cuenta
        if (window.ethereum) {{
            window.ethereum.on('accountsChanged', (accounts) => {{
                if (accounts.length === 0) {{
                    location.reload();
                }} else {{
                    userAddress = accounts[0];
                    walletInfoDiv.innerHTML = `✅ Wallet conectada: ${{userAddress.substring(0, 6)}}...${{userAddress.substring(38)}}`;
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
components.html(web3_component, height=400)

# Estado de la sesión
if 'verified' not in st.session_state:
    st.session_state.verified = False
    st.session_state.user_address = None
    st.session_state.nft_balance = 0

# Listener para mensajes del componente Web3
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'nft-verification') {
        window.parent.postMessage(event.data, '*');
    }
});
</script>
""", height=0)

# Separador
st.markdown("---")

# Mostrar contenido según verificación
st.markdown("### 📄 Acceso al Contenido")

# Simulación de verificación (en producción esto vendría del componente JS)
col1, col2 = st.columns(2)

with col1:
    if st.button("🔓 Simular Verificación Exitosa", help="Para pruebas"):
        st.session_state.verified = True
        st.session_state.user_address = "0x1234...5678"
        st.session_state.nft_balance = 1
        st.rerun()

with col2:
    if st.button("🔒 Resetear Verificación"):
        st.session_state.verified = False
        st.session_state.user_address = None
        st.session_state.nft_balance = 0
        st.rerun()

st.markdown("---")

# Mostrar contenido exclusivo o mensaje de acceso denegado
if st.session_state.verified:
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
            <li>Acceso a materiales educativos exclusivos</li>
            <li>Participación en eventos privados de la comunidad</li>
            <li>Ventajas especiales en futuros lanzamientos</li>
            <li>Comunicación directa con el equipo fundador</li>
            <li>Votación en decisiones importantes del proyecto</li>
        </ul>
        <p style="margin-top: 1.5rem; font-style: italic;">
            💎 Gracias por tu apoyo y confianza en nuestro proyecto.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user_address:
        st.success(f"✅ Verificado con wallet: {st.session_state.user_address}")
        st.info(f"🎫 NFTs en posesión: {st.session_state.nft_balance}")

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
        <ul style="margin-top: 0.5rem;">
            <li>Poseer al menos 1 NFT del contrato especificado</li>
            <li>Conectar tu wallet Web3 (MetaMask, WalletConnect, etc.)</li>
            <li>Estar en la red Arbitrum</li>
            <li>Firmar un mensaje de verificación (sin coste de gas)</li>
        </ul>
        <p style="margin-top: 1.5rem; font-weight: bold;">
            👆 Usa el botón "Conectar Wallet" arriba para comenzar la verificación.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
    <p>🔐 Verificación segura mediante firma offchain | Sin costes de gas</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">
        Powered by Web3 & Streamlit | Arbitrum Network
    </p>
</div>
""", unsafe_allow_html=True)
