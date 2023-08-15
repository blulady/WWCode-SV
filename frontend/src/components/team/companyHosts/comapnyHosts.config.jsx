import React from "react";
import WwcApi from "../../../WwcApi";
import ChevronUp from "../../../icons/ChevronUp";
import ChevronDown from "../../../icons/ChevronDown"
import Dropdown from "../../common/Dropdown";
import TruncatedText from "../companyHosts/TruncatedText";
import ModalDialog from "../../common/ModalDialog";
import styles from "./CompanyHosts.index.module.css";

export const columns = [
  {
    key: "id",
    title: "",
    dataIndex: "id",
  },
  {
    key: "company",
    title: "Company",
    dataIndex: "company",
  },
  {
    key: "city",
    title: "City",
    dataIndex: "city",
  },
  {
    key: "contacts",
    title: "Contacts",
    dataIndex: "contacts",
    render: (data, record) => {
      console.log(data);
      return data.map((item, index) => {
        console.log(item);
        return (
          <div key={index}>
            <Dropdown
              menuStyle={{ "max-width": "150px", backgroundColor: 'rgba(130, 130, 130, 0.1)' }}
              menu={[
                {
                  label: <a className="dropdown-item">{item.email}</a>,
                  key: 1,
                },
                {
                  label: <a className="dropdown-item">{item.info}</a>,
                  key: 2,
                },
                {
                  label: <hr class={["dropdown-divider", styles["contactsDivider"]].join(" ")} />,
                  key: 3,
                },
                {
                  label: <a className={["dropdown-item", styles["arrowUp"]].join(" ")}><ChevronDown /></a>,
                  key: 4,
                },
              ]}
            >
              <div className={["d-flex justify-content-between align-items-center", styles.contacts].join(" ")}>
                {item.name}{" "}
                <ChevronUp />
              </div>
            </Dropdown>
          </div>
        );
      });
    },
  },
  {
    key: "notes",
    title: "Notes",
    dataIndex: "notes",
    render: (notes) => {
      return <TruncatedText text={notes} />;
    },
  },
  {
    key: "actions",
    title: "Actions",
    dataIndex: "",
    render: (_, record) => {
      const handleDeleteCompanyHost = (companyId) => {
        WwcApi.deleteCompanyHost(companyId).catch((err) => {
          console.log(err);
        });
      };
      return (
        <ModalDialog
          id="deleteCompanyHost"
          title="Are you sure?"
          text="Are you sure you want to delete the company host?"
          onConfirm={() => handleDeleteCompanyHost(record.id)}
        >
          <button
            className={styles["delete"] + " " + styles["icon"]}
            type="button"
          />
        </ModalDialog>
      );
    },
  },
];
