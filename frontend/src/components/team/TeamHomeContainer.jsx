import React, { useState, useContext, useEffect } from 'react';
import WwcApi from '../../WwcApi';
import ContainerWithNav from "../layout/ContainerWithNav";
import styles from "./TeamHomeContainer.module.css";
import cx from "classnames";
import { NavLink, Outlet, useParams, useLocation } from 'react-router-dom';
import { useTeamContext } from '../../context/team/TeamContext';
import AuthContext from "../../context/auth/AuthContext";

const TeamHomeContainer = () => {
  const params = useParams();
  const team = parseInt(params.team);
  const { teams } = useTeamContext();
  const teamInfo = teams[team];
  const { userInfo } = useContext(AuthContext);
  const isDirector = userInfo.role === "DIRECTOR";
  const [user, setUser] = useState({});
  
  useEffect(() => {
    const getMember = async () => {
      try {
        const user = await WwcApi.getMember(userInfo.id);
        setUser(user);
      } catch (error) {
        console.warn("An error occurred while fetching user:", error.message);
      }
    };
    getMember();
  }, [userInfo.id]);

  const location = useLocation();
  let pageId = 0;
  teamInfo.pages.forEach((p, index) => {
    if (location.pathname.indexOf(p.pageId) > -1) {
      pageId = index;
    }
  });

  const [currentPage, setCurrentPage] = useState(pageId);

  return (
    <ContainerWithNav>
      <div
        id='teamHomeContainer'
        className={cx(styles["team-home-container"], "d-flex flex-column")}
      >
        <div className={styles["team-home-container-inner"]}>
          <div className={styles["team-home-tab-container"]}>
            {
              teamInfo.pages.map((page, i) => {
                if (page.type === 'externalLink') {
                  return (
                    <a href={page.link} target="_blank" rel="noopener" key={i}>
                      <button className={styles["tab-button"]}>
                        {page.label}
                      </button>
                    </a>
                  );
                }
                if (
                  (!page.isDirectorOnly || isDirector) 
                  && (!page.isHostTeamOnly || user?.role_teams?.some(team => team.team_name === teamInfo.name))
                ) {
                  return (
                    <NavLink to={`/team/${team}/${page.pageId}`} key={i}>
                      <button
                        className={styles["tab-button"] + (i === currentPage ? " " + styles["tab-button-selected"] : '')}
                        onClick={() => setCurrentPage(i)}
                      >
                        {page.label}
                      </button>
                    </NavLink>
                  );
                }
              }
            )}
          </div>
          <div
            className={cx(styles["team-home-tab-contents"], "d-flex flex-column")}
          >
            <Outlet />
          </div>
        </div>
      </div>
    </ContainerWithNav>
  );
};

export default TeamHomeContainer;
