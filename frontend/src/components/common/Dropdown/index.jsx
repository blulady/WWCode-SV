import React, { useState } from "react";

const Dropdown = ({ menu, menuStyle=null, children }) => {

  const [open, setOpen] = useState(false);

  const toggleDropdown = (e) => {
    e.stopPropagation();
    setOpen(!open);
  };

  const closeDropdown = () => setOpen(false)

  return (
    <>
      {React.cloneElement(children, {
        "data-bs-toggle": 'dropdown',
        "aria-expanded": "false",
        onClick: (e) => toggleDropdown(e),
      })}
      <ul className={`dropdown-menu ${open ? "show" : ""} dropdown-menu-lg-start`} style={menuStyle}>
        {menu.map((item) => (
          <li key={item.key} onClick={closeDropdown}>{item.label}</li>
        ))}
      </ul>
    </>
  );
};

export default Dropdown;
