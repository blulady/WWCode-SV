import React from "react";

const Dropdown = ({ menu, children }) => {
  return (
    <div className="dropdown">
      <ul className="dropdown-menu">
        {menu.map((item) => (
          <li key={item.key}>
            {item.label}
          </li>
        ))}
      </ul>
      {React.cloneElement(children, {
          "data-bs-toggle":"dropdown",
          "aria-expanded": "false"
      })}
    </div>
  );
};

export default Dropdown;
