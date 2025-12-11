import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import PlaylistInput from './PlaylistInput'


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="app-container">
        <h1 style={{ position: 'absolute', top: '10px', left: '560px' , color:'#F5FFFA'}}>Playlist Analyzer</h1>

        <p style={{ position: 'absolute', top: '150px', left: '320px', color:'#C1E1C1', fontSize:'25px' }}>“En sevdiğiniz şarkılarla dolu listenizin analizini çıkarın ve müzik tarzınızı keşfedin.”</p>

        <div className="input-wrapper" style={{ marginTop: '20px' }}>
          <PlaylistInput onAnalyze={(id) => console.log(id)} />
        </div>
      </div>
    </>
  )
}

export default App
