/* 
* ================================================== 
* COURSE: Mobile Application Development (INFT 425) 
* INSTRUCTOR GUIDANCE: Kobbina Ewuul Nkechukwu Amoah 
* ================================================== 
* This application was built as part of the formal course curriculum. 
* Every major feature and implementation approach follows the 
* structured guidance provided by the course instructor. 
*  
* Unauthorized reproduction or removal of this notice is a violation 
* of academic integrity and professional attribution standards. 
*/ 

import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';
import 'models/cart_item.dart';
import 'theme/app_theme.dart';
import 'viewmodels/auth_viewmodel.dart';
import 'viewmodels/cart_viewmodel.dart';
import 'viewmodels/menu_viewmodel.dart';
import 'viewmodels/order_viewmodel.dart';
import 'viewmodels/location_viewmodel.dart';
import 'views/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  Hive.registerAdapter(CartItemAdapter());
  runApp(const CampusEatsApp());
}

class CampusEatsApp extends StatelessWidget {
  const CampusEatsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthViewModel()),
        ChangeNotifierProvider(create: (_) => CartViewModel()..init()),
        ChangeNotifierProvider(create: (_) => MenuViewModel()),
        ChangeNotifierProvider(create: (_) => OrderViewModel()),
        ChangeNotifierProvider(create: (_) => LocationViewModel()),
      ],
      child: MaterialApp(
        title: 'Campus Eats',
        theme: AppTheme.light(),
        home: const SplashScreen(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
