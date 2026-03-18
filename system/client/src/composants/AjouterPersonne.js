import { useState } from "react";

const AjouterPersonne = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nom, setNom] = useState("");
  const [role, setRole] = useState("");

const handleAdd = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:8001/endpoint/add_collaborator`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, nom, role }),
      });
      if (res.ok) alert("Collaborateur ajouté !");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleAdd} className="space-y-4 p-4 border rounded">
      <h3 className="text-sm font-bold">Ajouter un collaborateur</h3>
      <input
        type="email"
        placeholder="Email"
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Mot de passe"
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setPassword(e.target.value)}
      />

       <input
        type="text"
        placeholder="Nom complet"
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setNom(e.target.value)}
      />

         <select
        className="w-full p-2 border text-sm rounded"
        onChange={(e) => setRole(e.target.value)}
      >
        <option value="member">Membre</option>
        <option value="admin">Admin</option>
      </select>


      <button className="bg-blue-600 text-white px-4 py-2 rounded text-xs">
        Ajouter
      </button>
    </form>
  );
}
export default AjouterPersonne;
