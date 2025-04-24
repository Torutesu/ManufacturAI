import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, NavLink } from 'react-router-dom';
import './App.css';

// ページコンポーネントのインポート
import Dashboard from './pages/Dashboard';
import QualityInspection from './pages/QualityInspection';
import InventoryManagement from './pages/InventoryManagement';
import MaterialNesting from './pages/MaterialNesting';
import ProductionManagement from './pages/ProductionManagement';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="logo">
            <h1>ManufacturAI</h1>
          </div>
          <ul className="nav-links">
            <li>
              <NavLink exact to="/" activeClassName="active">
                ダッシュボード
              </NavLink>
            </li>
            <li>
              <NavLink to="/quality" activeClassName="active">
                品質検査
              </NavLink>
            </li>
            <li>
              <NavLink to="/inventory" activeClassName="active">
                在庫管理
              </NavLink>
            </li>
            <li>
              <NavLink to="/material" activeClassName="active">
                建材・ネスティング
              </NavLink>
            </li>
            <li>
              <NavLink to="/production" activeClassName="active">
                生産管理
              </NavLink>
            </li>
          </ul>
        </nav>

        <main className="content">
          <Switch>
            <Route exact path="/" component={Dashboard} />
            <Route path="/quality" component={QualityInspection} />
            <Route path="/inventory" component={InventoryManagement} />
            <Route path="/material" component={MaterialNesting} />
            <Route path="/production" component={ProductionManagement} />
          </Switch>
        </main>
      </div>
    </Router>
  );
}

export default App;
