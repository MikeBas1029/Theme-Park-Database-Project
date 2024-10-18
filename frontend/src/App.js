import {Routes, Route} from "react-router-dom"
import { DisplayModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Navbar from "./scenes/global/Navbar";
import Sidebar from "./scenes/global/Sidebar";
//import Staff from "./scenes/Staff";
//import Transactions from "./scenes/Transactions";
//import Rides from "./scenes/Rides";
//import Security from "./scenes/Security";
//import Calendar from "./scenes/Calendar";
import Dashboard from "./scenes/dashboard/index";
import LoginForm from "./scenes/login/LoginForm";




function App() {
  const [theme, colorMode] = useMode();
  return ( 
  <DisplayModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Sidebar />
       <main className="content">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />}/> {/* Dashboard routing */}
          <Route path="/login" element={<LoginForm />} />   {/*Login page routing */}
        </Routes>

      </main>
      </div>
    </ThemeProvider>
  </DisplayModeContext.Provider>
  );
}

export default App;
