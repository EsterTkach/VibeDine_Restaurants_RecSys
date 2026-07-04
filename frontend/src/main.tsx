import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { AuthProvider } from "./contexts/AuthContext";
import { HomeProvider } from "./contexts/HomeContext.tsx";

// createRoot(document.getElementById("root")!).render(
//   <StrictMode>
//     <AuthProvider>
//       <HomeProvider>
//       <App />
//       </HomeProvider>
//     </AuthProvider>
//   </StrictMode>,
// );

createRoot(document.getElementById("root")!).render(
    <AuthProvider>
      <HomeProvider>
      <App />
      </HomeProvider>
    </AuthProvider>
);
