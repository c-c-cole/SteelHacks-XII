function About() {
  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center", color: "#2A3F7D" }}>About Civic Compass</h1>
      <p style={{ textAlign: "center", color: "#5A7FFF", fontStyle: "italic" }}>
        "Making Pittsburgh more accessible for everyone."
      </p>
      <p>
        Civic Compass is a civic-focused tool that allows users to explore accessibility
        of public amenities—like hospitals, parks, and community centers—across the
        city. Users can view metrics, post comments, and see areas where access
        improvements are most needed.
      </p>
      <p>
        The app combines public transportation data, bike accessibility, and
        neighborhood demographics to highlight underserved areas and support
        better urban planning decisions.
      </p>
      <p style={{ fontStyle: "italic", textAlign: "center" }}>
        Developed during SteelHacks XII.
      </p>
    </div>
  );
}

export default About;
