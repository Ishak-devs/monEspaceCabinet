import { useState } from "react";

function EmailAuto() {

  const [candidate, setCandidate] = useState("");
  const [mail, setMail] = useState("");
  const [notes_email, setNotes] = useState("");
  const [remuneration, setRemuneration] = useState("");
  const [poste, setPoste] = useState("");
  const [doc, setDoctosend] = useState("");
  const [prochaine_etape, setProchain_etape] = useState("");
  const [lieu, setLieu] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8001/envoyer-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nom: candidate,
          email: mail,
          notes_mail: notes_email,
          poste: poste,
          doc: doc,
          prochaine_etape: prochaine_etape,
          lieu: lieu,
        }),
      });
      if (response.ok) alert("Email envoyé !");
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <section className="p-6 border border-blue-100 rounded-lg bg-blue-50/30">
        <h3 className="text-sm font-semibold mb-4 flex items-center">
          <span className="mr-2">🚀</span> Email automatisé
        </h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="Nom du candidat"
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setCandidate(e.target.value)}
          />
           <input
            type="text"
            placeholder="Intitulé d'offre"
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setPoste(e.target.value)}
          />
          <input
            type="text"
            placeholder="Lieu"
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setLieu(e.target.value)}
          />
          <input
            type="text"
            placeholder="Rémunération"
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setRemuneration(e.target.value)}
          />
          <input
            type="text"
            placeholder="Document a transmettre..."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setDoctosend(e.target.value)}
          />
            <input
            type="text"
            placeholder="Prochaines étapes.."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setProchain_etape(e.target.value)}
          />
          <input
            type="text"
            placeholder="Notes personnalisés..."
            className="flex-1 p-2 text-sm border rounded shadow-sm focus:ring-1 focus:ring-blue-500 outline-none"
            onChange={(e) => setNotes(e.target.value)}
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-xs font-medium transition-colors disabled:bg-gray-400"
          >
            {loading ? "Envoi..." : "Envoyer"}
          </button>
        </div>
      </section>
    </div>
  );
}
export default EmailAuto;