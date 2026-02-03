import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

function Prospection() {
  const [intitule, setIntitule] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // const [currentStatus, setCurrentStatus] = useState("");
  const [prospection, setProspection] = useState([]);
  // const [expandedProspection, setExpandedProspection] = useState(null);
  // const [statusMessage, setStatusMessage] = useState("");
  const [itemToDelete, setItemToDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const [statusLogs, setStatusLogs] = useState(() => {
    const saved = localStorage.getItem("prospection_logs");
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    const activeProspection = prospection.find((p) => p.is_active === true);
    if (prospection.length > 0 && !activeProspection) {
      setStatusLogs([]);
      localStorage.removeItem("prospection_logs");
    }
  }, [prospection]); // ceci pour raffraichir a chaque fois que la liste change

  const FetchProspection = async () => {
    try {
      const res = await fetch(
        "http://localhost:8000/backend/prospection/list",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
          },
        },
      );
      const data = await res.json();
      setProspection(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  useEffect(() => {
    FetchProspection();
    const timer = setInterval(() => {
      FetchProspection();
    }, 10000);

    return () => clearInterval(timer);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!intitule.trim()) return;

    setIsLoading(true);
    setStatusLogs([]);
    localStorage.removeItem("prospection_logs");

    try {
      const response = await fetch(
        "http://localhost:8000/backend/prospection/start_prospection",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ intitule }),
        },
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        console.log("Reçu:", chunk);

        setStatusLogs((prev) => {
          const newLogs = [...prev, chunk];
          localStorage.setItem("prospection_logs", JSON.stringify(newLogs));
          return newLogs;
        });
      }

      if (response.ok) {
        setIntitule("");
        FetchProspection();
      }
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredProspection = prospection.filter((p) =>
    p.job_title?.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="min-h-screen bg-white p-4 md:p-6 font-sans">
      <div className="max-w-5xl mx-auto">
        <div className="mb-6">
          <h1 className="text-lg font-normal text-gray-900 tracking-tight">
            Prospection
          </h1>
          <p className="text-gray-500 text-xs mt-0.5">
            Gestion des prospections
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Formulaire compact */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded border border-gray-200 p-4">
              <h2 className="text-sm font-normal text-gray-900 mb-4">
                Nouvelle prospection
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label
                    htmlFor="intitule"
                    className="block text-xs font-normal text-gray-600 mb-1.5"
                  >
                    Intitulé du métier
                  </label>
                  <input
                    id="intitule"
                    type="text"
                    value={intitule}
                    onChange={(e) => setIntitule(e.target.value)}
                    disabled={isLoading}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:outline-none focus:border-gray-400 disabled:bg-gray-50"
                    placeholder="Ex: Développeur Front-end"
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading || !intitule.trim()}
                  className={`w-full py-2 text-xs rounded transition-colors
                    ${
                      isLoading || !intitule.trim()
                        ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                        : "bg-black hover:bg-gray-800 text-white"
                    }`}
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                      Traitement...
                    </span>
                  ) : (
                    "Lancer la prospection"
                  )}
                </button>
                <p className="text-gray-500 text-xs mt-0.5">
                  N'actualisez pas la page durant une prospection
                </p>
              </form>
            </div>
          </div>

          {/* Liste sobre */}
          <div className="lg:col-span-2">
            <div className="bg-white border border-gray-200 rounded">
              {/* En-tête minimal */}
              <div className="p-4 border-b border-gray-100">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h2 className="text-sm font-normal text-gray-900">
                      Historique
                    </h2>
                    <p className="text-gray-500 text-xs mt-0.5">
                      {prospection.length} prospection
                      {prospection.length !== 1 ? "s" : ""}
                    </p>
                  </div>
                  <div className="relative">
                    <input
                      type="text"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full sm:w-48 px-3 py-1.5 text-xs bg-white border border-gray-300 rounded shadow-none outline-none"
                      placeholder="Rechercher..."
                    />

                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                    {statusLogs.length > 0 && (
                      <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded text-[10px] font-mono max-h-40 overflow-y-auto">
                        <p className="text-gray-400 mb-1">Logs en direct :</p>
                        {statusLogs.map((log, index) => (
                          <div
                            key={index}
                            className="text-blue-600 border-l-2 border-blue-200 pl-2 mb-1"
                          >
                            {log}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Liste compacte */}
              <div className="divide-y divide-gray-100 max-h-[500px] overflow-y-auto">
                {filteredProspection.length === 0 ? (
                  <div className="p-6 text-center">
                    <svg
                      className="w-8 h-8 text-gray-300 mx-auto mb-3"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                    <p className="text-gray-400 text-xs">
                      {searchTerm ? "Aucun résultat" : "Aucune prospection"}
                    </p>
                  </div>
                ) : (
                  filteredProspection.map((p) => (
                    <div
                      key={p.id}
                      // className={`p-3 hover:bg-gray-50 transition-colors ${
                      //   expandedProspection === p.id ? "bg-gray-50" : ""
                      // }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1.5">
                            <h3 className="text-xs font-normal text-gray-900 truncate">
                              {p.job_title}
                            </h3>

                            {p.is_active && (
                              <div className="flex items-center text-blue-600">
                                <div className="animate-spin rounded-full h-3 w-3 border-2 border-current border-t-transparent"></div>
                                {/* <p className="text-gray-500 text-xs mt-0.5">
                                  {statusMessage || "En attente..."}
                                </p>*/}
                              </div>
                            )}
                          </div>

                          <div className="flex items-center text-gray-400 text-[10px] gap-3">
                            <span className="flex items-center">
                              <svg
                                className="w-2.5 h-2.5 mr-1"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                                />
                              </svg>
                              {new Date(p.created_at).toLocaleDateString(
                                "fr-FR",
                                {
                                  day: "numeric",
                                  month: "short",
                                  year: "numeric",
                                },
                              )}
                            </span>
                            <span className="flex items-center">
                              <svg
                                className="w-2.5 h-2.5 mr-1"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                              </svg>
                              {new Date(p.created_at).toLocaleTimeString(
                                "fr-FR",
                                {
                                  hour: "2-digit",
                                  minute: "2-digit",
                                },
                              )}
                            </span>
                          </div>
                        </div>

                        <button
                          onClick={() => setItemToDelete(p.id)}
                          className="text-gray-300 hover:text-red-500 p-1 transition-colors ml-2"
                        >
                          <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      {itemToDelete && (
        <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-sm w-full shadow-xl">
            <h3 className="text-sm font-medium text-gray-900">
              Supprimer la prospection ?
            </h3>
            <p className="text-xs text-gray-500 mt-2">
              La suppression est définitive
            </p>
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => setItemToDelete(null)}
                className="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded"
              >
                Annuler
              </button>
              <button
                onClick={async () => {
                  await supabase
                    .from("prospection_settings")
                    .delete()
                    .eq("id", itemToDelete);
                  setItemToDelete(null);
                  FetchProspection();
                }}
                className="px-3 py-1.5 text-xs bg-red-600 text-white hover:bg-red-700 rounded"
              >
                Confirmer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Prospection;

// import { useState, useEffect, useRef } from "react";
// import { supabase } from "../supabaseClient";

// function Prospection() {
//   const [intitule, setIntitule] = useState("");
//   const [isLoading, setIsLoading] = useState(false);
//   const [prospection, setProspection] = useState([]);
//   const [itemToDelete, setItemToDelete] = useState(null);
//   const [searchTerm, setSearchTerm] = useState("");
//   const [statusLogs, setStatusLogs] = useState(() => {
//     const saved = localStorage.getItem("prospection_logs");
//     return saved ? JSON.parse(saved) : [];
//   });
//   const [notification, setNotification] = useState(null);
//   const logsEndRef = useRef(null);

//   useEffect(() => {
//     if (statusLogs.length > 0) {
//       setTimeout(() => {
//         logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
//       }, 100);
//     }
//   }, [statusLogs]);

//   useEffect(() => {
//     const activeProspection = prospection.find((p) => p.is_active === true);
//     if (prospection.length > 0 && !activeProspection) {
//       setStatusLogs([]);
//       localStorage.removeItem("prospection_logs");
//     }
//   }, [prospection]);

//   const FetchProspection = async () => {
//     try {
//       const res = await fetch(
//         "http://localhost:8000/backend/prospection/list",
//         {
//           method: "GET",
//           headers: {
//             "Content-Type": "application/json",
//             "ngrok-skip-browser-warning": "true",
//           },
//         },
//       );
//       const data = await res.json();
//       setProspection(Array.isArray(data) ? data : []);
//     } catch (error) {
//       console.error("Erreur:", error);
//       showNotification("Erreur lors du chargement", "error");
//     }
//   };

//   useEffect(() => {
//     FetchProspection();
//     const timer = setInterval(() => {
//       FetchProspection();
//     }, 10000);

//     return () => clearInterval(timer);
//   }, []);

//   const showNotification = (message, type = "info") => {
//     setNotification({ message, type });
//     setTimeout(() => setNotification(null), 4000);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!intitule.trim()) {
//       showNotification("Veuillez saisir un intitulé", "warning");
//       return;
//     }

//     setIsLoading(true);
//     setStatusLogs([]);
//     localStorage.removeItem("prospection_logs");

//     try {
//       const response = await fetch(
//         "http://localhost:8000/backend/prospection/start_prospection",
//         {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ intitule }),
//         },
//       );

//       if (!response.ok) {
//         throw new Error("Erreur serveur");
//       }

//       const reader = response.body.getReader();
//       const decoder = new TextDecoder();

//       while (true) {
//         const { value, done } = await reader.read();
//         if (done) break;
//         const chunk = decoder.decode(value, { stream: true });

//         setStatusLogs((prev) => {
//           const newLogs = [...prev, chunk];
//           localStorage.setItem("prospection_logs", JSON.stringify(newLogs));
//           return newLogs;
//         });
//       }

//       setIntitule("");
//       FetchProspection();
//       showNotification("Prospection terminée", "success");
//     } catch (error) {
//       console.error("Erreur:", error);
//       showNotification("Erreur lors de la prospection", "error");
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleDelete = async (id) => {
//     try {
//       await supabase.from("prospection_settings").delete().eq("id", id);
//       setItemToDelete(null);
//       FetchProspection();
//       showNotification("Prospection supprimée", "success");
//     } catch (error) {
//       console.error("Erreur:", error);
//       showNotification("Erreur lors de la suppression", "error");
//     }
//   };

//   const filteredProspection = prospection.filter((p) =>
//     p.job_title?.toLowerCase().includes(searchTerm.toLowerCase()),
//   );

//   const activeCount = prospection.filter((p) => p.is_active === true).length;

//   return (
//     <div className="min-h-screen bg-gray-50 p-6 font-sans">
//       {/* Notification */}
//       {notification && (
//         <div className="fixed top-4 right-4 z-50 animate-fadeIn">
//           <div
//             className={`px-4 py-3 rounded border ${
//               notification.type === "success"
//                 ? "bg-emerald-50 border-emerald-200 text-emerald-700"
//                 : notification.type === "error"
//                   ? "bg-rose-50 border-rose-200 text-rose-700"
//                   : notification.type === "warning"
//                     ? "bg-amber-50 border-amber-200 text-amber-700"
//                     : "bg-slate-50 border-slate-200 text-slate-700"
//             }`}
//           >
//             <div className="flex items-center gap-2 text-sm">
//               {notification.type === "success" && (
//                 <svg
//                   className="w-4 h-4"
//                   fill="currentColor"
//                   viewBox="0 0 20 20"
//                 >
//                   <path
//                     fillRule="evenodd"
//                     d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
//                     clipRule="evenodd"
//                   />
//                 </svg>
//               )}
//               {notification.type === "error" && (
//                 <svg
//                   className="w-4 h-4"
//                   fill="currentColor"
//                   viewBox="0 0 20 20"
//                 >
//                   <path
//                     fillRule="evenodd"
//                     d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
//                     clipRule="evenodd"
//                   />
//                 </svg>
//               )}
//               {notification.message}
//             </div>
//           </div>
//         </div>
//       )}

//       <div className="max-w-7xl mx-auto">
//         {/* Header */}
//         <div className="mb-8">
//           <h1 className="text-lg font-normal text-slate-900">Prospection</h1>
//           <p className="text-slate-500 text-sm mt-1">
//             Gestion des prospections
//           </p>

//           {activeCount > 0 && (
//             <div className="mt-4 text-xs text-amber-600 bg-amber-50 border border-amber-100 inline-flex items-center px-3 py-1.5 rounded">
//               <span className="w-1.5 h-1.5 bg-amber-500 rounded-full mr-2 animate-pulse"></span>
//               Prospection en cours - Veuillez ne pas actualiser la page
//             </div>
//           )}
//         </div>

//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
//           {/* Left Column */}
//           <div className="lg:col-span-1 space-y-6">
//             {/* Form Card */}
//             <div className="bg-white rounded-sm border border-slate-200 p-5">
//               <div className="mb-6">
//                 <h2 className="text-sm font-medium text-slate-900 mb-1">
//                   Nouvelle prospection
//                 </h2>
//                 <p className="text-slate-500 text-xs">
//                   Lancez une nouvelle recherche
//                 </p>
//               </div>

//               <form onSubmit={handleSubmit} className="space-y-5">
//                 <div>
//                   <label className="block text-xs font-medium text-slate-700 mb-2">
//                     Intitulé du métier
//                   </label>
//                   <input
//                     type="text"
//                     value={intitule}
//                     onChange={(e) => setIntitule(e.target.value)}
//                     disabled={isLoading}
//                     className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-sm focus:outline-none focus:border-slate-400 focus:ring-1 focus:ring-slate-400 transition-colors disabled:bg-slate-50"
//                     placeholder="ex: Développeur Front-end"
//                     required
//                   />
//                 </div>

//                 <button
//                   type="submit"
//                   disabled={isLoading || !intitule.trim()}
//                   className={`w-full py-2.5 text-sm font-medium rounded-sm transition-colors ${
//                     isLoading || !intitule.trim()
//                       ? "bg-slate-100 text-slate-400 cursor-not-allowed"
//                       : "bg-slate-900 hover:bg-slate-800 text-white"
//                   }`}
//                 >
//                   {isLoading ? (
//                     <span className="flex items-center justify-center">
//                       <svg
//                         className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
//                         fill="none"
//                         viewBox="0 0 24 24"
//                       >
//                         <circle
//                           className="opacity-25"
//                           cx="12"
//                           cy="12"
//                           r="10"
//                           stroke="currentColor"
//                           strokeWidth="4"
//                         />
//                         <path
//                           className="opacity-75"
//                           fill="currentColor"
//                           d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//                         />
//                       </svg>
//                       Traitement...
//                     </span>
//                   ) : (
//                     "Lancer la prospection"
//                   )}
//                 </button>
//               </form>
//             </div>

//             {/* Live Logs */}
//             {statusLogs.length > 0 && (
//               <div className="bg-white rounded-sm border border-slate-200 p-5">
//                 <div className="flex items-center justify-between mb-4">
//                   <h3 className="text-sm font-medium text-slate-900">
//                     Logs en direct
//                   </h3>
//                   <span className="text-xs text-slate-500">
//                     {statusLogs.length}
//                   </span>
//                 </div>

//                 <div className="bg-slate-50 rounded-sm p-3 h-64 overflow-y-auto">
//                   <div className="space-y-2 text-xs font-mono">
//                     {statusLogs.map((log, index) => (
//                       <div
//                         key={index}
//                         className={`p-2 rounded border-l-2 ${
//                           log.toLowerCase().includes("erreur")
//                             ? "border-rose-500 bg-rose-50 text-rose-700"
//                             : log.toLowerCase().includes("terminé") ||
//                                 log.toLowerCase().includes("succès")
//                               ? "border-emerald-500 bg-emerald-50 text-emerald-700"
//                               : "border-blue-500 bg-blue-50 text-blue-700"
//                         }`}
//                       >
//                         <div className="flex">
//                           <span className="text-slate-500 mr-2 flex-shrink-0">
//                             {new Date().toLocaleTimeString([], {
//                               hour: "2-digit",
//                               minute: "2-digit",
//                             })}
//                           </span>
//                           <span className="flex-1 truncate">{log}</span>
//                         </div>
//                       </div>
//                     ))}
//                     <div ref={logsEndRef} />
//                   </div>
//                 </div>
//               </div>
//             )}
//           </div>

//           {/* Right Column - History */}
//           <div className="lg:col-span-2">
//             <div className="bg-white rounded-sm border border-slate-200">
//               {/* Header */}
//               <div className="p-5 border-b border-slate-100">
//                 <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
//                   <div>
//                     <h2 className="text-sm font-medium text-slate-900">
//                       Historique
//                     </h2>
//                     <p className="text-slate-500 text-xs mt-1">
//                       {prospection.length} prospection
//                       {prospection.length !== 1 ? "s" : ""}
//                       {activeCount > 0 && ` • ${activeCount} en cours`}
//                     </p>
//                   </div>

//                   <div className="relative">
//                     <input
//                       type="text"
//                       value={searchTerm}
//                       onChange={(e) => setSearchTerm(e.target.value)}
//                       className="w-full sm:w-56 px-3 py-2 text-sm bg-white border border-slate-300 rounded-sm focus:outline-none focus:border-slate-400 focus:ring-1 focus:ring-slate-400"
//                       placeholder="Rechercher..."
//                     />
//                   </div>
//                 </div>
//               </div>

//               {/* List */}
//               <div className="divide-y divide-slate-100">
//                 {filteredProspection.length === 0 ? (
//                   <div className="p-8 text-center">
//                     <div className="text-slate-300 mb-3">
//                       <svg
//                         className="w-8 h-8 mx-auto"
//                         fill="none"
//                         stroke="currentColor"
//                         viewBox="0 0 24 24"
//                       >
//                         <path
//                           strokeLinecap="round"
//                           strokeLinejoin="round"
//                           strokeWidth={1}
//                           d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
//                         />
//                       </svg>
//                     </div>
//                     <p className="text-slate-500 text-sm">
//                       {searchTerm
//                         ? "Aucune prospection trouvée"
//                         : "Aucune prospection"}
//                     </p>
//                   </div>
//                 ) : (
//                   filteredProspection.map((p) => (
//                     <div
//                       key={p.id}
//                       className={`p-4 hover:bg-slate-50 transition-colors ${
//                         p.is_active ? "bg-blue-50" : ""
//                       }`}
//                     >
//                       <div className="flex items-center justify-between">
//                         <div className="flex-1 min-w-0">
//                           <div className="flex items-center gap-2 mb-1">
//                             <h3 className="text-sm font-medium text-slate-900 truncate">
//                               {p.job_title}
//                             </h3>

//                             {p.is_active && (
//                               <span className="inline-flex items-center">
//                                 <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-1.5 animate-pulse"></span>
//                                 <span className="text-xs text-blue-600">
//                                   En cours
//                                 </span>
//                               </span>
//                             )}
//                           </div>

//                           <div className="flex items-center text-slate-500 text-xs gap-4">
//                             <span className="flex items-center gap-1">
//                               <svg
//                                 className="w-3 h-3"
//                                 fill="none"
//                                 stroke="currentColor"
//                                 viewBox="0 0 24 24"
//                               >
//                                 <path
//                                   strokeLinecap="round"
//                                   strokeLinejoin="round"
//                                   strokeWidth={1.5}
//                                   d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
//                                 />
//                               </svg>
//                               {new Date(p.created_at).toLocaleDateString(
//                                 "fr-FR",
//                               )}
//                             </span>
//                             <span className="flex items-center gap-1">
//                               <svg
//                                 className="w-3 h-3"
//                                 fill="none"
//                                 stroke="currentColor"
//                                 viewBox="0 0 24 24"
//                               >
//                                 <path
//                                   strokeLinecap="round"
//                                   strokeLinejoin="round"
//                                   strokeWidth={1.5}
//                                   d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
//                                 />
//                               </svg>
//                               {new Date(p.created_at).toLocaleTimeString(
//                                 "fr-FR",
//                                 {
//                                   hour: "2-digit",
//                                   minute: "2-digit",
//                                 },
//                               )}
//                             </span>
//                           </div>
//                         </div>

//                         <div className="flex items-center gap-2">
//                           <button
//                             onClick={() => setItemToDelete(p.id)}
//                             className="p-1 text-slate-400 hover:text-rose-500 transition-colors"
//                             title="Supprimer"
//                           >
//                             <svg
//                               className="w-4 h-4"
//                               fill="none"
//                               stroke="currentColor"
//                               viewBox="0 0 24 24"
//                             >
//                               <path
//                                 strokeLinecap="round"
//                                 strokeLinejoin="round"
//                                 strokeWidth={1.5}
//                                 d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
//                               />
//                             </svg>
//                           </button>
//                         </div>
//                       </div>
//                     </div>
//                   ))
//                 )}
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Delete Modal */}
//       {itemToDelete && (
//         <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4">
//           <div className="bg-white rounded-sm border border-slate-200 p-6 max-w-sm w-full">
//             <div className="mb-4">
//               <h3 className="text-sm font-medium text-slate-900 mb-1">
//                 Supprimer la prospection ?
//               </h3>
//               <p className="text-slate-500 text-xs">
//                 Cette action ne peut pas être annulée.
//               </p>
//             </div>

//             <div className="flex justify-end gap-2">
//               <button
//                 onClick={() => setItemToDelete(null)}
//                 className="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded-sm transition-colors"
//               >
//                 Annuler
//               </button>
//               <button
//                 onClick={() => handleDelete(itemToDelete)}
//                 className="px-4 py-2 text-sm bg-rose-600 text-white hover:bg-rose-700 rounded-sm transition-colors"
//               >
//                 Supprimer
//               </button>
//             </div>
//           </div>
//         </div>
//       )}

//       <style jsx>{`
//         @keyframes fadeIn {
//           from {
//             opacity: 0;
//             transform: translateY(-10px);
//           }
//           to {
//             opacity: 1;
//             transform: translateY(0);
//           }
//         }

//         .animate-fadeIn {
//           animation: fadeIn 0.2s ease-out;
//         }
//       `}</style>
//     </div>
//   );
// }

// export default Prospection;
