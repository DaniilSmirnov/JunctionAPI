import React, {Component, useRef} from "react";
import Carousel from 'nuka-carousel';
import { motion, useMotionValue, useTransform } from "framer-motion"
import PropTypes from 'prop-types';
import "../styles/styles.css"
import connect from '@vkontakte/vk-connect';
import fetchJsonp from 'fetch-jsonp';
import Panel from '@vkontakte/vkui/dist/components/Panel/Panel';
import PanelHeader from '@vkontakte/vkui/dist/components/PanelHeader/PanelHeader';
import Button from '@vkontakte/vkui/dist/components/Button/Button';
import Group from '@vkontakte/vkui/dist/components/Group/Group';
import Cell from '@vkontakte/vkui/dist/components/Cell/Cell';
import Div from '@vkontakte/vkui/dist/components/Div/Div';
import Avatar from '@vkontakte/vkui/dist/components/Avatar/Avatar';
//import {data} from '../data/categories';
import Swipe from 'react-easy-swipe';

class StartScreen extends React.Component {

    constructor(props) {
        super(props);

         this.state = {
			activePanel: 'StartScreen',
			categories: this.props.categories,
			authToken: this.props.authToken,
			number: 0
		}
		
	}
	
	componentDidMount(){
		console.log(this.props.categories);
	}

    render(){
		
		{console.log(this.state.categories)}
		{console.log(this.state.authToken)}
		return (
			<Panel id="StartScreen">
			{this.state.categories.map((c)=>(
			<div className="deck">
				<div className="card">
				<div className="cardHeader">
					{/*{this.state.c.name}*/}
				</div>
			</div>
			</div>
			))}
			</Panel>	

		);
    }
}

export default StartScreen;
