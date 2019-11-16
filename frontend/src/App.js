import React from 'react';
import { View } from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';
import connect from '@vkontakte/vk-connect';

import Icon28Newsfeed from '@vkontakte/icons/dist/28/newsfeed';
import Icon28RecentOutline from '@vkontakte/icons/dist/28/recent_outline';
import Icon28InfoOutline from '@vkontakte/icons/dist/28/info_outline';
import Icon28Settings from '@vkontakte/icons/dist/28/settings';

import StartScreen from './panels/StartScreen';

import { platform, IOS, ANDROID } from '@vkontakte/vkui';
import {Epic, Tabbar, TabbarItem} from '@vkontakte/vkui';

const osname = platform();

class App extends React.Component {
	constructor (props) {
		super(props);
	
		this.state = {
			activeStory: 'StartScreen',
			fetchedUser: null,
			authToken: null,
			categories:[4,5]
		};
		this.onStoryChange = this.onStoryChange.bind(this);
	}
	
	componentDidMount(){
		connect.subscribe((e) => {
			switch (e.detail.type) {
				case 'VKWebAppGetUserInfoResult':
					this.setState({ fetchedUser: e.detail.data});
					console.log('test');
					break;	
				case 'VKWebAppAccessTokenReceived':
					console.log('test2');
					this.setState({ authToken: e.detail.data.access_token });
					connect.send("VKWebAppCallAPIMethod", {"method": "junction.getCategories", "request_id": "32test", "params": {"count": "10", "v":"5.103", "access_token": this.state.authToken}});
					break;
				case 'VKWebAppCallAPIMethodResult':
					console.log('tes3');
					this.setState({categories : e.detail.data.response});
					console.log(this.state.categories);
					break;
				default:
					console.log("Data: "+e.detail.data);
			}
		});	
		connect.send('VKWebAppInit');
		connect.send("VKWebAppGetAuthToken", {"app_id": 7210275, "scope": "groups"});

	}

	  onStoryChange (e) {
		this.setState({ activeStory: e.currentTarget.dataset.story })
	  }

	  go = (e) => {
		this.setState({ activePanel: e.currentTarget.dataset.to })
		};

		updateData = (value1, value2) => {
			this.setState({groupName: value1,
			groupId:value2})
		}

		saveOffsets = (value1, value2) => {
			this.setState({offset1: value1,
				offset2:value2})
		}

	  render () {
			console.log(this.state.authToken);
			return (
				<Epic scheme={this.state.scheme} activeStory={this.state.activeStory} tabbar={
				<Tabbar>
					<TabbarItem
					onClick={this.onStoryChange}
					selected={this.state.activeStory === 'StartScreen'}
					data-story="StartScreen"
					text="Категории"
					><Icon28Newsfeed /></TabbarItem>
						
				</Tabbar>
				}>
				<View id="StartScreen" activePanel="StartScreen">
					<StartScreen id="StartScreen" fetchedUser={this.state.fetchedUser} categories={this.state.categories} authToken={this.state.authToken}/>
				</View>
				
				</Epic>
			)
	  }
	}
export default App;