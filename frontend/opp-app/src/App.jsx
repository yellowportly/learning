import { useState, useEffect } from "react";
import "./styles.css";

export default function App() {
  const API_URL_ALL = "http://localhost:8000/opportunities"; // For JSON Server
  const API_URL_SINGLE = "http://localhost:8000/opportunity"; // For JSON Server
  const [items, setItems] = useState([]);
  const [formData, setFormData] = useState(
      {
          opportunity_id: null,
          title: null,
          url: null,
          industry: null,
          status: null,
          application_text: null
      });
  const [loading, setLoading] = useState(false);

  const fetchItems = async () => {
    setLoading(true);
    const res = await fetch(API_URL_ALL);
    const data = await res.json();
    setItems(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleChange = (e) => {
      //
    setFormData({ ...formData, [e.target.name]: e.target.value });
    console.log("HandleChange: " + JSON.stringify(e));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.opportunity_id) {
        console.log("HandleSubmit: " + JSON.stringify(formData))
      await fetch(`${API_URL_SINGLE}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
            {
                opportunity_id: formData.opportunity_id,
                title: formData.title,
                url: formData.url,
                industry: formData.industry,
                application_text: formData.application_text,
                status: formData.status
            }),
      });
    } else {
      await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: formData.title }),
      });
    }
    setFormData({
        opportunity_id: null,
          title: null,
          url: null,
          industry: null,
          status: null,
          application_text: null });
    fetchItems();
  };

  // const handleDelete = async (opportunity_id) => {
  //   await fetch(`${API_URL}/${opportunity_id}`, { method: "DELETE" });
  //   fetchItems();
  // };

  const handleEdit = (item) => {
      console.log("HandleEdit: " + JSON.stringify(item))
    setFormData(
        {
            opportunity_id: item.opportunity_id,
            title: item.title,
            url: item.url,
            industry: item.industry,
            application_text: item.application_text,
            status: item.status
        });
  };

  return (
    <div className="container">
      <h1>Opportunity app</h1>
      <form onSubmit={handleSubmit}>
          <fieldset>
              <legend>Opportunity data</legend>
              <p>
                  <label className='field' for="opportunity_id">Opportunity id:</label>
                  <input
                      name="opportunity_id"
                      value={formData.opportunity_id}
                      onChange={handleChange}
                      placeholder="Enter opportunity id"
                      required/>
              </p>
              <p>
                  <label className='field' for="title">Title:</label>
                  <input
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      placeholder="Enter title"
                      required/>
              </p>
              <p>
                  <label className='field' for="url">Url:</label>
                  <input
                      name="url"
                      value={formData.url}
                      onChange={handleChange}
                      placeholder="Enter URL"
                      required/>
              </p>
              <p>
                  <label className='field' for="industry">Industry:</label>
                  <input
                      name="industry"
                      value={formData.industry}
                      onChange={handleChange}
                      placeholder="Enter Industry"
                      required/>
              </p>
              <p>
                  <label className='field' for="url">Status:</label>
                  <input
                      name="status"
                      value={formData.status}
                      onChange={handleChange}
                      placeholder="Enter Status"
                      required/>
              </p>
              <p>
                  <label className='field' for="application_text">Application text:</label>
                  <textarea
                      name="application_text"
                      value={formData.application_text}
                      rows={4}
                      cols={60}
                      onChange={handleChange}
                      placeholder="Application text"
                      required/>
              </p>

              <button type="submit" className="add">
                  {formData.opportunity_id ? "Update" : "Add"}
              </button>
          </fieldset>
      </form>

        {loading ? (
            <p>Loading...</p>
        ) : (
            <ul>
                {items.map((item) => (
                    <li key={item.opportunity_id}>
                        <span>{item.title} ({item.opportunity_id})</span>
                        <div>
                            <button className="edit" onClick={() => handleEdit(item)}>
                                Edit
                            </button>
                <button className="delete" onClick={() => handleDelete(item.opportunity_id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
