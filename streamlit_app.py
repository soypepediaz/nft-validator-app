import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="NFT Token Gated - Diagnóstico",
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
st.markdown('<h1 class="main-title">🔍 Diagnóstico de Wallet</h1>', unsafe_allow_html=True)

st.warning("**Modo Diagnóstico:** Esta versión mostrará información detallada sobre qué wallets detecta tu navegador.")

# Información
with st.expander("ℹ️ Información del NFT"):
    st.write(f"**Red:** Arbitrum One")
    st.write(f"**Contrato:** `{NFT_CONTRACT_ADDRESS}`")

# Estado de sesión
if 'nft_verified' not in st.session_state:
    st.session_state.nft_verified = False
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = None
if 'nft_balance' not in st.session_state:
    st.session_state.nft_balance = 0

# Componente de diagnóstico detallado
diagnostic_component = f"""
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
            font-family: 'Courier New', monospace;
            padding: 20px;
            background: #f8f9fa;
            font-size: 13px;
        }}
        .diagnostic-box {{
            background: white;
            border: 2px solid #007bff;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        .diagnostic-title {{
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #007bff;
        }}
        .check-item {{
            padding: 8px;
            margin: 5px 0;
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
            border-radius: 4px;
        }}
        .check-item.success {{
            border-left-color: #28a745;
            background: #d4edda;
        }}
        .check-item.error {{
            border-left-color: #dc3545;
            background: #f8d7da;
        }}
        .check-item.warning {{
            border-left-color: #ffc107;
            background: #fff3cd;
        }}
        .button {{
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
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
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
        }}
        .button:disabled {{
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
        }}
        .code-block {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 10px 0;
            font-size: 12px;
            line-height: 1.5;
        }}
        .wallet-info {{
            background: linear-gradient(135deg, #8697FF15 0%, #7C5AFF15 100%);
            padding: 18px;
            border-radius: 10px;
            margin: 15px 0;
            border: 2px solid #8697FF;
        }}
        .status {{
            margin: 15px 0;
            padding: 18px;
            border-radius: 10px;
            font-size: 15px;
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
        .spinner {{
            border: 3px solid #f3f3f3;
            border-top: 3px solid #007bff;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="diagnostic-box">
        <div class="diagnostic-title">🔍 DIAGNÓSTICO DE WALLETS</div>
        <div id="diagnosticOutput">Iniciando diagnóstico...</div>
    </div>

    <button id="runDiagnostic" class="button">🔬 Ejecutar Diagnóstico Completo</button>
    <button id="connectBtn" class="button" style="display:none;">🐰 Conectar con Rabby</button>
    <button id="verifyBtn" class="button" style="display:none;" disabled>🔍 Verificar NFT</button>
    
    <div id="status"></div>
    <div id="walletInfo"></div>

    <script>
        const NFT_ADDRESS = '{NFT_CONTRACT_ADDRESS}';
        const ARBITRUM_RPC = 'https://arb1.arbitrum.io/rpc';
        const CHAIN_ID = {CHAIN_ID};
        const CHAIN_ID_HEX = '{CHAIN_ID_HEX}';
        
        const ERC721_ABI = [{{"inputs": [{{"internalType": "address", "name": "owner", "type": "address"}}], "name": "balanceOf", "outputs": [{{"internalType": "uint256", "name": "", "type": "uint256"}}], "stateMutability": "view", "type": "function"}}];
        
        let web3;
        let userAddress;
        let rabbyProvider = null;

        const diagnosticOutput = document.getElementById('diagnosticOutput');
        const runDiagnostic = document.getElementById('runDiagnostic');
        const connectBtn = document.getElementById('connectBtn');
        const verifyBtn = document.getElementById('verifyBtn');
        const statusDiv = document.getElementById('status');
        const walletInfoDiv = document.getElementById('walletInfo');

        function showStatus(message, type) {{
            statusDiv.className = `status status-${{type}}`;
            statusDiv.innerHTML = message;
            statusDiv.style.display = 'block';
        }}

        function addDiagnosticItem(message, type) {{
            const div = document.createElement('div');
            div.className = `check-item ${{type}}`;
            div.innerHTML = message;
            diagnosticOutput.appendChild(div);
        }}

        function addCodeBlock(title, code) {{
            const div = document.createElement('div');
            div.innerHTML = `<strong style="display:block;margin:10px 0 5px 0;">${{title}}:</strong><div class="code-block">${{code}}</div>`;
            diagnosticOutput.appendChild(div);
        }}

        function runFullDiagnostic() {{
            diagnosticOutput.innerHTML = '';
            addDiagnosticItem('🔄 Iniciando diagnóstico completo...', 'warning');
            
            // 1. Verificar window.ethereum
            if (typeof window.ethereum !== 'undefined') {{
                addDiagnosticItem('✅ window.ethereum existe', 'success');
                
                // Inspeccionar propiedades de window.ethereum
                const ethereumProps = [];
                for (let prop in window.ethereum) {{
                    if (prop.toLowerCase().includes('rabbit') || 
                        prop.toLowerCase().includes('rabby') ||
                        prop === 'isRabby' || 
                        prop === 'isMetaMask' ||
                        prop === 'isBraveWallet' ||
                        prop === 'isOkxWallet' ||
                        prop === 'isPhantom' ||
                        prop === 'isCoinbaseWallet') {{
                        ethereumProps.push(`  ${{prop}}: ${{window.ethereum[prop]}}`);
                    }}
                }}
                
                if (ethereumProps.length > 0) {{
                    addCodeBlock('Propiedades de window.ethereum', ethereumProps.join('\\n'));
                }} else {{
                    addDiagnosticItem('⚠️ No se encontraron flags de wallet conocidas en window.ethereum', 'warning');
                }}
                
                // Verificar providers array
                if (window.ethereum.providers && Array.isArray(window.ethereum.providers)) {{
                    addDiagnosticItem(`✅ window.ethereum.providers existe [${{window.ethereum.providers.length}} proveedor(es)]`, 'success');
                    
                    window.ethereum.providers.forEach((provider, index) => {{
                        const providerInfo = [];
                        providerInfo.push(`Proveedor [${{index}}]:`);
                        
                        if (provider.isRabby) providerInfo.push('  ✅ isRabby: true');
                        if (provider.isMetaMask) providerInfo.push('  ⚠️ isMetaMask: true');
                        if (provider.isBraveWallet) providerInfo.push('  ⚠️ isBraveWallet: true');
                        if (provider.isOkxWallet) providerInfo.push('  ⚠️ isOkxWallet: true');
                        if (provider.isPhantom) providerInfo.push('  ⚠️ isPhantom: true');
                        
                        addCodeBlock(``, providerInfo.join('\\n'));
                    }});
                }} else {{
                    addDiagnosticItem('❌ window.ethereum.providers NO existe o no es array', 'error');
                }}
                
            }} else {{
                addDiagnosticItem('❌ window.ethereum NO existe', 'error');
            }}
            
            // 2. Verificar window.rabby directo
            if (typeof window.rabby !== 'undefined') {{
                addDiagnosticItem('✅ window.rabby existe (MÉTODO PREFERIDO)', 'success');
                rabbyProvider = window.rabby;
            }} else {{
                addDiagnosticItem('❌ window.rabby NO existe', 'error');
            }}
            
            // 3. Verificar objetos alternativos
            const alternativeObjects = ['okxwallet', 'phantom', 'coinbaseWalletExtension', 'trustwallet'];
            let foundAlternatives = [];
            alternativeObjects.forEach(obj => {{
                if (typeof window[obj] !== 'undefined') {{
                    foundAlternatives.push(obj);
                }}
            }});
            
            if (foundAlternatives.length > 0) {{
                addDiagnosticItem(`⚠️ Otras wallets detectadas: ${{foundAlternatives.join(', ')}}`, 'warning');
                addCodeBlock('RECOMENDACIÓN', 'Desactiva estas wallets en brave://extensions/ para evitar conflictos');
            }}
            
            // 4. Detectar Rabby específicamente
            let rabbyFound = false;
            let rabbyMethod = '';
            
            if (typeof window.rabby !== 'undefined') {{
                rabbyProvider = window.rabby;
                rabbyFound = true;
                rabbyMethod = 'window.rabby';
            }} else if (typeof window.ethereum !== 'undefined') {{
                if (window.ethereum.isRabby) {{
                    rabbyProvider = window.ethereum;
                    rabbyFound = true;
                    rabbyMethod = 'window.ethereum.isRabby';
                }} else if (window.ethereum.providers) {{
                    for (let provider of window.ethereum.providers) {{
                        if (provider.isRabby) {{
                            rabbyProvider = provider;
                            rabbyFound = true;
                            rabbyMethod = 'window.ethereum.providers[i].isRabby';
                            break;
                        }}
                    }}
                }}
            }}
            
            // 5. Resultado final
            addDiagnosticItem('═══════════════════════════════════════', '');
            
            if (rabbyFound) {{
                addDiagnosticItem(`✅ RABBY DETECTADA mediante: ${{rabbyMethod}}`, 'success');
                addDiagnosticItem('✅ Puedes continuar con la conexión', 'success');
                connectBtn.style.display = 'block';
                runDiagnostic.style.display = 'none';
            }} else {{
                addDiagnosticItem('❌ RABBY NO DETECTADA', 'error');
                addCodeBlock('POSIBLES CAUSAS', 
                    '1. Rabby no está instalada\\n' +
                    '2. Rabby está desactivada en brave://extensions/\\n' +
                    '3. Otra wallet está sobrescribiendo window.ethereum\\n' +
                    '4. Necesitas refrescar la página después de instalar Rabby'
                );
                addCodeBlock('SOLUCIÓN', 
                    '1. Ve a brave://extensions/\\n' +
                    '2. Verifica que Rabby esté activada (toggle azul)\\n' +
                    '3. DESACTIVA todas las otras wallets\\n' +
                    '4. Refresca esta página (F5)\\n' +
                    '5. Ejecuta el diagnóstico nuevamente'
                );
            }}
            
            // 6. Información del navegador
            addDiagnosticItem('═══════════════════════════════════════', '');
            addCodeBlock('Información del Navegador',
                `User Agent: ${{navigator.userAgent}}\\n` +
                `Plataforma: ${{navigator.platform}}\\n` +
                `Idioma: ${{navigator.language}}`
            );
        }}

        runDiagnostic.addEventListener('click', runFullDiagnostic);

        // Ejecutar diagnóstico automáticamente al cargar
        window.addEventListener('load', () => {{
            setTimeout(runFullDiagnostic, 500);
        }});

        connectBtn.addEventListener('click', async () => {{
            if (!rabbyProvider) {{
                showStatus('❌ Error: Rabby provider no disponible', 'error');
                return;
            }}

            try {{
                connectBtn.disabled = true;
                showStatus('🔄 Conectando con Rabby...', 'info');
                
                const accounts = await rabbyProvider.request({{ 
                    method: 'eth_requestAccounts' 
                }});
                
                if (!accounts || accounts.length === 0) {{
                    throw new Error('No se obtuvieron cuentas');
                }}
                
                userAddress = accounts[0];
                
                showStatus('🔄 Cambiando a Arbitrum...', 'info');
                
                try {{
                    await rabbyProvider.request({{
                        method: 'wallet_switchEthereumChain',
                        params: [{{ chainId: CHAIN_ID_HEX }}],
                    }});
                }} catch (switchError) {{
                    if (switchError.code === 4902) {{
                        await rabbyProvider.request({{
                            method: 'wallet_addEthereumChain',
                            params: [{{
                                chainId: CHAIN_ID_HEX,
                                chainName: 'Arbitrum One',
                                nativeCurrency: {{ name: 'Ethereum', symbol: 'ETH', decimals: 18 }},
                                rpcUrls: ['https://arb1.arbitrum.io/rpc'],
                                blockExplorerUrls: ['https://arbiscan.io/']
                            }}]
                        }});
                    }} else {{
                        throw switchError;
                    }}
                }}

                web3 = new Web3(rabbyProvider);
                
                walletInfoDiv.className = 'wallet-info';
                walletInfoDiv.innerHTML = `
                    <div><strong>🐰 Rabby Conectada</strong></div>
                    <div style="font-family: monospace; margin-top: 5px;">${{userAddress}}</div>
                `;
                
                connectBtn.style.display = 'none';
                verifyBtn.style.display = 'block';
                verifyBtn.disabled = false;
                showStatus('✅ Conexión exitosa', 'success');
                
            }} catch (error) {{
                console.error('Error:', error);
                showStatus(`❌ Error: ${{error.message}}`, 'error');
                connectBtn.disabled = false;
            }}
        }});

        verifyBtn.addEventListener('click', async () => {{
            try {{
                verifyBtn.disabled = true;
                showStatus('🔄 Verificando NFT...', 'info');

                const message = `Verificar NFT\\nWallet: ${{userAddress}}\\nContrato: ${{NFT_ADDRESS}}\\nTimestamp: ${{Date.now()}}`;
                const signature = await web3.eth.personal.sign(message, userAddress);

                const arbitrumWeb3 = new Web3(ARBITRUM_RPC);
                const contract = new arbitrumWeb3.eth.Contract(ERC721_ABI, NFT_ADDRESS);
                const balance = await contract.methods.balanceOf(userAddress).call();
                const balanceNum = parseInt(balance);
                
                if (balanceNum > 0) {{
                    showStatus(`✅ Verificado! Tienes ${{balanceNum}} NFT(s)`, 'success');
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{ success: true, address: userAddress, balance: balanceNum }}
                    }}, '*');
                }} else {{
                    showStatus('❌ No posees este NFT', 'error');
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: {{ success: false, address: userAddress, balance: 0 }}
                    }}, '*');
                }}
            }} catch (error) {{
                showStatus(`❌ Error: ${{error.message}}`, 'error');
            }} finally {{
                verifyBtn.disabled = false;
            }}
        }});
    </script>
</body>
</html>
"""

# Renderizar componente
verification_result = components.html(diagnostic_component, height=800, scrolling=True)

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

# Mostrar contenido
if st.session_state.nft_verified:
    st.markdown("""
    <div class="exclusive-content">
        <h2>🎉 ¡Contenido Exclusivo Desbloqueado!</h2>
        <p>Felicidades por ser parte de nuestra comunidad de NFT holders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.wallet_address:
        st.success(f"✅ Verificado: `{st.session_state.wallet_address}`")
        st.info(f"🎫 NFTs: **{st.session_state.nft_balance}**")
else:
    st.markdown("""
    <div class="error-box">
        <h3>🔒 Contenido Exclusivo para Token Holders</h3>
        <p>Primero ejecuta el diagnóstico para verificar la detección de Rabby.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 **Tip:** Este modo diagnóstico te mostrará exactamente qué wallets detecta tu navegador y por qué Rabby no está siendo reconocida.")
