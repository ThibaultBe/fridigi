import { Stack } from 'expo-router';
import { FlatList, Text, View, StyleSheet } from 'react-native';


export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#DBF0FA',
        },
        headerTintColor: '#0F266C',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
      {/* Optionally configure static options outside the route.*/}
      <Stack.Screen name="index" 
      options={{
        title: 'Fridigi',
            headerLargeTitle: true, // iOS only - creates the large title effect
            headerTitleStyle: {
              fontWeight: 'bold',
              fontSize:24, // Increase font size
          
            },

      }} />
    </Stack>
  );
}

