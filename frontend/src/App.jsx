import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AnalysisProvider } from './context/AnalysisContext';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <AnalysisProvider>
      <Router>
        <div className="flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
          </main>
          <Footer />
        </div>
        <Toaster 
          position="bottom-right"
          toastOptions={{
            style: {
              background: '#1A1D29',
              color: '#FAFAFA',
              border: '1px solid rgba(108, 99, 255, 0.2)',
            },
            success: {
              iconTheme: {
                primary: '#00D4AA',
                secondary: '#1A1D29',
              },
            },
          }}
        />
      </Router>
    </AnalysisProvider>
  );
}

export default App;
