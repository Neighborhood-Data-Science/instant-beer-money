import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ScrapeButton from './components/initalScrape_button.tsx'
import ShowButton from './components/showTable_button'

function App() {
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>
        </p>
        <ScrapeButton />
        <ShowButton />
      </div>
    </>
  )
}

export default App
