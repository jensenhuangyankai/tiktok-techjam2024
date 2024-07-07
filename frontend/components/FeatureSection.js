"use client";

const FeatureSection = ({ title, description }) => {
  return (
    <section className="p-10 bg-white border-b border-gray-300 text-center text-black">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <p className="text-base">{description}</p>
    </section>
  );
};

export default FeatureSection;
