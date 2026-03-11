import { useState, useEffect } from "react";
import { supabase } from "../supabaseClient";

const css = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; background: #f8f8f7; }
  .wrap { max-width: 860px; margin: 40px auto; padding: 0 24px; }
  h2 { font-size: 16px; font-weight: 500; margin-bottom: 4px; }
  .sub { font-size: 11px; color: #999; margin-bottom: 24px; }
  .grid { display: grid; grid-template-columns: 1fr 1.6fr; gap: 20px; }
  .card { background: #fff; border: 1px solid #e8e8e8; border-radius: 10px; padding: 20px; }
  input[type=text] { width: 100%; padding: 8px 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 12px; margin-bottom: 10px; outline: none; background: #fafafa; }
  input[type=text]:focus { border-color: #aaa; background: #fff; }
  .radios { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
  .radios label { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #555; cursor: pointer; }
  .btn { width: 100%; padding: 9px; background: #111; color: #fff; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; margin-top: 4px; }
  .btn:disabled { background: #eee; color: #aaa; cursor: not-allowed; }
  .row { display: flex; justify-content: space-between; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
  .row:last-child { border: none; }
  .tag { display: inline-block; font-size: 10px; padding: 2px 7px; border-radius: 20px; background: #eff6ff; color: #3b82f6; margin-left: 6px; }
  .del { background: none; border: none; color: #ccc; cursor: pointer; font-size: 14px; padding: 2px 6px; }
  .del:hover { color: #ef4444; }
  .logs { font-size: 10px; font-family: monospace; color: #3b82f6; margin-top: 6px; max-height: 80px; overflow-y: auto; background: #f5f8ff; border-radius: 4px; padding: 6px; }
  .modal-bg { position: fixed; inset: 0; background: rgba(0,0,0,0.25); display: flex; align-items: center; justify-content: center; }
  .modal { background: #fff; border-radius: 10px; padding: 24px; min-width: 260px; }
  .modal p { font-size: 13px; margin-bottom: 16px; }
  .modal-btns { display: flex; justify-content: flex-end; gap: 10px; }
  .modal-btns button { padding: 6px 14px; border-radius: 6px; font-size: 12px; cursor: pointer; border: none; }
  .modal-btns .cancel { background: #f0f0f0; color: #333; }
  .modal-btns .confirm { background: #ef4444; color: #fff; }
`;

export default function ProspectionSourcing() {
  const [f, setF] = useState({ intitule: "", segment: "", mode: "", details: "", candidat: "", post: "", search: "" });
  const [list, setList] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [del, setDel] = useState(null);

  const headers = async () => {
    const { data: { session } } = await supabase.auth.getSession();
    return { "Content-Type": "application/json", Authorization: `Bearer ${session?.access_token}` };
  };

  const fetchList = async () => {
    const r = await fetch("http://127.0.0.1:8001/backend/prospection/list", { headers: await headers() });
    setList(await r.json().catch(() => []));
  };

  useEffect(() => { fetchList(); const t = setInterval(fetchList, 10000); return () => clearInterval(t); }, []);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true); setLogs([]);
    const r = await fetch("http://127.0.0.1:8001/backend/linkedin/start_chrome", {
      method: "POST", headers: await headers(),
body: JSON.stringify({
  intitule: f.intitule,
  details: f.details,
  mode: f.mode,
  candidatrecherche: f.candidat,
  post: f.post,
  segment: f.segment,
  telephone: "",
  full_name: ""
}),
    });
    const reader = r.body.getReader(), dec = new TextDecoder();
    while (true) { const { value, done } = await reader.read(); if (done) break; setLogs(l => [...l, dec.decode(value)]); }
    setLoading(false); fetchList();
  };

  const s = k => e => setF(p => ({ ...p, [k]: e.target.value }));
  const active = list.some(p => p.is_active);
  const filtered = list.filter(p => p.job_title?.toLowerCase().includes(f.search.toLowerCase()));

  return (
    <>
      <style>{css}</style>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"/>
      <div className="wrap">
        <h2>Prospection & Sourcing</h2>
        <p className="sub">LinkedIn · Gestion</p>
        <div className="grid">

          <div className="card">
            <form onSubmit={submit}>
              <div className="radios">
                {["Entreprises","Offres","Annonces","Personnes"].map(v =>
                  <label key={v}><input type="radio" name="seg" value={v} onChange={s("segment")} disabled={loading}/> {v}</label>
                )}
              </div>
              {[["post","Indication posts"],["intitule","Intitulé du métier"],["details","Détails messages (IA)"]].map(([k,ph]) =>
                <input key={k} type="text" placeholder={ph} value={f[k]} onChange={s(k)} disabled={loading}/>
              )}
              <div className="radios" style={{marginBottom:12}}>
                {["Prospection","sourcing"].map(v =>
                  <label key={v}><input type="radio" name="mode" value={v} onChange={s("mode")} required disabled={loading}/> {v}</label>
                )}
              </div>
              {f.mode === "sourcing" && <input type="text" placeholder="Profil recherché" value={f.candidat} onChange={s("candidat")} disabled={loading}/>}
              <button className="btn" type="submit" disabled={loading || !f.intitule.trim() || active}>
                {loading ? "En cours..." : "Lancer"}
              </button>
            </form>
          </div>

          <div className="card">
            <input type="text" placeholder="Rechercher..." onChange={s("search")} style={{marginBottom:12}}/>
            <div style={{maxHeight:420, overflowY:"auto"}}>
              {filtered.length === 0
                ? <p style={{fontSize:12, color:"#bbb", textAlign:"center", padding:20}}>Aucune prospection</p>
                : filtered.map(p => (
                  <div className="row" key={p.id}>
                    <div>
                      <span style={{fontSize:13, fontWeight:500}}>{p.job_title}</span>
                      {p.is_active && <span className="tag">● actif</span>}
                      {p.is_active && logs.length > 0 && <div className="logs">{logs.map((l,i) => <div key={i}>{l}</div>)}</div>}
                    </div>
                    <button className="del" onClick={() => setDel(p.id)}>✕</button>
                  </div>
                ))}
            </div>
          </div>

        </div>
      </div>

      {del && (
        <div className="modal-bg">
          <div className="modal">
            <p>Supprimer cette prospection ?</p>
            <div className="modal-btns">
              <button className="cancel" onClick={() => setDel(null)}>Annuler</button>
              <button className="confirm" onClick={async () => { await supabase.from("prospection_settings").delete().eq("id", del); setDel(null); fetchList(); }}>Confirmer</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}