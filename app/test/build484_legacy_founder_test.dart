import 'package:flutter_test/flutter_test.dart';
import 'package:ngelx_app/main.dart';

void main() {
  test('Build484: verified legacy founder retains manager permissions', () {
    final community = <String, dynamic>{
      'founderId': 'founder',
      'members': <String>['founder', 'admin', 'ordinary'],
      'admins': <String>['admin'],
      'moderators': <String>['ordinary'],
    };
    expect(ngelx484CommunityManager(community, 'founder'), isTrue);
    expect(ngelx484CommunityManager(community, 'admin'), isTrue);
    expect(ngelx457CanEditCover(community, 'founder'), isTrue);
    expect(ngelx457CanEditCover(community, 'admin'), isTrue);
  });

  test('Build484: normal members and moderators are never promoted', () {
    final community = <String, dynamic>{
      'founderId': 'founder',
      'members': <String>['founder', 'admin', 'member', 'moderator'],
      'admins': <String>['admin'],
      'moderators': <String>['moderator'],
    };
    for (final uid in ['member', 'moderator', 'stranger', '']) {
      expect(ngelx484CommunityManager(community, uid), isFalse);
      expect(ngelx457CanEditCover(community, uid), isFalse);
    }
  });

  test('Build484: stale or removed founder cannot manage a community', () {
    final community = <String, dynamic>{
      'founderId': 'formerFounder',
      'members': <String>['admin', 'member'],
      'admins': <String>['admin'],
    };
    expect(ngelx484CommunityManager(community, 'formerFounder'), isFalse);
    expect(ngelx457CanEditCover(community, 'formerFounder'), isFalse);
    expect(ngelx484CommunityManager(community, 'admin'), isTrue);
  });

  test('Build484: regular contemporary founder continues to be recognized', () {
    final community = <String, dynamic>{
      'founderId': 'founder',
      'members': <String>['founder', 'member'],
      'admins': <String>['founder'],
    };
    expect(ngelx484CommunityManager(community, 'founder'), isTrue);
    expect(ngelx484CommunityManager(community, 'member'), isFalse);
    expect(ngelx457CanEditCover(community, 'founder'), isTrue);
  });
}
